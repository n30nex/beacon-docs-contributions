"""Offline regression checks for the local stack helper; no GitHub/Pi access."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import beacon_stack as stack


class StackTests(unittest.TestCase):
    def test_missing_configured_guard_stops_before_commands(self):
        with tempfile.TemporaryDirectory(prefix='beacon-missing-guard-') as directory:
            root = Path(directory); manifest = root/'stack.json'
            stack.write(manifest, dict(guard_script=str(root/'missing.ps1')))
            with patch.object(stack, 'GUARD_SCRIPT', None), patch.object(stack, 'command', side_effect=AssertionError('must stop before commands')):
                with self.assertRaisesRegex(RuntimeError, 'guard is missing'):
                    stack.main('start', manifest, root/'state', branch='codex/next')

    def test_publication_rechecks_upstream_after_validation(self):
        manifest = dict(upstream='MeshCore-Beacon/beacon-web', fork='example/beacon-web', entries=[])
        class Result:
            stdout = 'new-upstream'
        with patch.object(stack, 'command', return_value=Result()):
            with self.assertRaisesRegex(RuntimeError, 'changed during validation'):
                stack.verify_publish_state(manifest, dict(base='old-upstream', entries=[]))
            stack.verify_publish_state(manifest, dict(base='new-upstream', entries=[]))

    def test_portable_guard_rejects_default_and_dirty_branches(self):
        with tempfile.TemporaryDirectory(prefix='beacon-guard-test-') as directory:
            repo = Path(directory); self.init_repo(repo); self.commit(repo, 'file.txt', 'base\n')
            stack.git(repo, 'checkout', '-B', 'dev')
            with patch.object(stack, 'GUARD_SCRIPT', None):
                with self.assertRaisesRegex(RuntimeError, 'isolated feature branch'):
                    stack.guard(repo, 'Preflight', repo/'receipt.json')
                stack.git(repo, 'checkout', '-b', 'codex/feature')
                (repo/'file.txt').write_text('dirty\n')
                with self.assertRaisesRegex(RuntimeError, 'isolated feature branch'):
                    stack.guard(repo, 'Preflight', repo/'receipt.json')

    def test_start_after_all_merges_uses_current_dev_without_rebase_or_build(self):
        with tempfile.TemporaryDirectory(prefix='beacon-start-test-') as directory:
            root = Path(directory); repo = root/'repo'; repo.mkdir(); self.init_repo(repo)
            old = self.commit(repo, 'file.txt', 'old\n')
            current = self.commit(repo, 'file.txt', 'accepted\n')
            stack.git(repo, 'remote', 'add', 'origin', 'https://github.com/MeshCore-Beacon/beacon-web.git')
            stack.git(repo, 'remote', 'add', 'contribution', 'https://github.com/example/beacon-web.git')
            stack.git(repo, 'update-ref', 'refs/remotes/origin/dev', current)
            manifest = root/'stack.json'
            stack.write(manifest, dict(repo='repo', upstream='MeshCore-Beacon/beacon-web', fork='example/beacon-web', remote='contribution', entries=[dict(pr=1, branch='codex/old', head=old, remote_head=old, base=old, worktree='repo')]))
            original = stack.command
            class Result:
                returncode = 0
                stdout = ''
            def fake_command(args, **kwargs):
                if args[0] == 'gh':
                    r = Result()
                    r.stdout = current if 'commits/dev' in args[2] else json.dumps(dict(merged=True, head=dict(repo=dict(full_name='example/beacon-web'))))
                    return r
                if args[:2] == ['git', 'fetch']:
                    return Result()
                if args[0] in ('npm', 'node', 'go', 'swag') or args[:2] == ['git', 'rebase']:
                    raise AssertionError('A fresh phase must not rebase or build')
                return original(args, **kwargs)
            with patch.object(stack, 'ROOT', root), patch.object(stack, 'GUARD_SCRIPT', None), patch.object(stack, 'command', fake_command):
                stack.main('start', manifest, root/'state', branch='codex/next')
            started = json.loads((root/'state/started.json').read_text())
            self.assertEqual(started['parent'], current)
            self.assertIsNone(started['depends_on'])
            self.assertEqual(stack.git(started['worktree'], 'rev-parse', 'HEAD').stdout.strip(), current)

    def test_remote_updates_and_closed_prs_stop_publication(self):
        entries = [dict(pr=1, branch='codex/one', remote_head='1'*40, head='1'*40, base='2'*40)]
        pull = dict(merged=False, state='open', head=dict(sha='1'*40, ref='codex/one'), base=dict(ref='dev'))
        self.assertEqual(len(stack.active_entries(entries, [pull])), 1)
        for changed in [dict(pull, state='closed'), dict(pull, head=dict(sha='someone-elses-work', ref='codex/one'))]:
            with self.assertRaises(RuntimeError):
                stack.active_entries(entries, [changed])
        self.assertEqual(stack.active_entries(entries, [dict(pull, merged=True, state='closed')]), [])
        with self.assertRaisesRegex(RuntimeError, 'exact commit IDs'):
            stack.active_entries([dict(entries[0], base='--exec=untrusted')], [pull])

    def test_squash_merges_then_drop_accepted_parent(self):
        with tempfile.TemporaryDirectory(prefix='beacon-stack-test-') as directory:
            repo = Path(directory)
            self.init_repo(repo)
            base = self.commit(repo, 'settings.go', 'base\n')
            first = self.commit(repo, 'settings.go', 'base\naccounts\n')
            second = self.commit(repo, 'settings.go', 'base\naccounts\nbackup\n')
            entries = [dict(pr=1, head=first, base=base), dict(pr=2, head=second, base=first)]
            proof = stack.simulate_squash_order(repo, base, entries)
            self.assertTrue(all(row['clean_after_squash_and_refresh'] for row in proof))
            tree = stack.git(repo, 'rev-parse', first+'^{tree}').stdout.strip()
            squash = stack.git(repo, 'commit-tree', tree, '-p', base, '-m', 'accepted first PR').stdout.strip()
            stack.git(repo, 'checkout', '-b', 'child', second)
            stack.rebase(repo, squash, first)
            self.assertEqual(stack.git(repo, 'rev-parse', 'HEAD^{tree}').stdout.strip(), proof[-1]['tree'])
            self.assertEqual(stack.git(repo, 'rev-list', '--count', squash+'..HEAD').stdout.strip(), '1')

    def test_source_conflict_is_left_for_review(self):
        with tempfile.TemporaryDirectory(prefix='beacon-stack-test-') as directory:
            repo = Path(directory)
            self.init_repo(repo)
            base = self.commit(repo, 'main.go', 'base\n')
            child = self.commit(repo, 'main.go', 'our change\n')
            stack.git(repo, 'checkout', '-b', 'upstream', base)
            upstream = self.commit(repo, 'main.go', 'different upstream change\n')
            stack.git(repo, 'checkout', '-b', 'candidate', child)
            with self.assertRaisesRegex(RuntimeError, 'Source conflict preserved'):
                stack.rebase(repo, upstream, base)
            self.assertEqual(stack.git(repo, 'diff', '--name-only', '--diff-filter=U').stdout.strip(), 'main.go')
            self.assertEqual(stack.git(repo, 'rev-parse', 'refs/heads/candidate').stdout.strip(), child)
            stack.git(repo, 'rebase', '--abort')

    def test_verified_tree_skips_builds(self):
        with tempfile.TemporaryDirectory(prefix='beacon-stack-cache-') as directory:
            cache = Path(directory)
            stack.write(cache/'tree.json', dict(passed=True, tools='go / swag', build_environment='{}'))
            class Result:
                stdout = ''
            def fake_git(repo, *args, **kwargs):
                result = Result()
                result.stdout = 'tree\n' if args[0] == 'rev-parse' else ''
                return result
            def fake_command(args, **kwargs):
                if args[:2] == ['go', 'env']:
                    result = Result(); result.stdout = '{}'; return result
                if args not in (['go', 'version'], ['swag', '--version']):
                    raise AssertionError('cached source tree unexpectedly rebuilt')
                result = Result(); result.stdout = args[0]
                return result
            with patch.object(stack, 'git', fake_git), patch.object(stack, 'command', fake_command):
                self.assertTrue(stack.validate(cache, cache)['reused'])

    def test_web_environment_fingerprint_changes_without_recording_values(self):
        with tempfile.TemporaryDirectory(prefix='beacon-web-cache-') as directory:
            root = Path(directory)
            first = stack.web_fingerprint(root)
            (root/'.env.local').write_text('VITE_FIXTURE=PRIVATE_CANARY\n', encoding='utf-8')
            second = stack.web_fingerprint(root)
            self.assertNotEqual(first, second)
            self.assertNotIn('PRIVATE_CANARY', second)
            self.assertEqual(len(second), 64)

    def test_preview_overlay_preserves_both_independent_changes(self):
        with tempfile.TemporaryDirectory(prefix='beacon-preview-test-') as directory:
            repo = Path(directory); self.init_repo(repo)
            base = self.commit(repo, 'base.txt', 'base\n')
            feature = self.commit(repo, 'analytics.txt', 'charts\n')
            stack.git(repo, 'checkout', '-b', 'overlay', base)
            overlay = self.commit(repo, 'nodes.txt', 'badges\n')
            tree = stack.preview_tree(repo, feature, [overlay])
            self.assertEqual(set(stack.git(repo, 'ls-tree', '--name-only', tree).stdout.splitlines()), {'base.txt', 'analytics.txt', 'nodes.txt'})

    @staticmethod
    def init_repo(repo):
        stack.git(repo, 'init', '-q')
        stack.git(repo, 'config', 'user.name', 'Stack test')
        stack.git(repo, 'config', 'user.email', 'test@example.invalid')
        stack.git(repo, 'config', 'core.autocrlf', 'false')

    @staticmethod
    def commit(repo, file, text):
        (repo/file).write_text(text, encoding='utf-8', newline='\n')
        stack.git(repo, 'add', file)
        stack.git(repo, 'commit', '-q', '-m', text.strip().replace('\n', ' '))
        return stack.git(repo, 'rev-parse', 'HEAD').stdout.strip()


if __name__ == '__main__':
    unittest.main()
