# Server/web consolidation release

Status: preparation, not a published release or a full CoreScope parity claim. Updated 20 September 2026 after maintainer review of the four server PRs.

## Scope and stop point

Finish the current account/backup/analytics queue, correct review regressions, and release that bounded set before Channel Activity or further parity expansion. Current public tags are server v1.6.0 and web v1.3.0; maintainers choose the next versions and perform signed release commits, main promotion and tags under each repository's contribution rules.

The deployment owner performs the eventual CoreScope switch. Beacon remains at dev.meshcore.ca, CoreScope at live.meshcore.ca, and the Pi preview remains at canadaverse.org/beacon-dev/ with its changelog and corresponding source.

Independent follow-up [server #160](https://github.com/MeshCore-Beacon/beacon-server/pull/160) adds offline archive verification and does not block or expand this release's required queue. Its separately installed Pi CLI is `262eae96`; the running server/web stay unchanged. Required native and compiled PostgreSQL checks pass, with Windows race coverage because the Pi race runtime cannot initialize. Decide explicitly whether to include the CLI follow-up when freezing the release; issue #72 remains partial either way.

Independent follow-up [server #161](https://github.com/MeshCore-Beacon/beacon-server/pull/161), `0befdc5c`, adds ACK/TRACE/PING summaries in the existing packet display and also leaves the release queue independent. It merges cleanly with the reviewed stack. Combined server `5848d200` is on the Pi with web `42ba5fcb`; native PostgreSQL, Windows race, CI and public REST/live/browser checks pass. No schema/config changes or extra public admin access. Include it only if accepted when freezing; #99 remains partial for other requested formats.

## Review gates

- [x] Server #149: document POST/DELETE browser preflights and the full admin CORS method example. Keep public read-only defaults.
- [x] Server #154: verify pg_dump/server compatibility at startup; an optional backup prerequisite failure disables only backup, with a specific operator diagnostic. Document backup.enabled and distinguish the export size limit. Native testing caught and fixed the text-versus-integer version-setting scan; CI now covers it with PostgreSQL.
- [x] Server #157: serve Signal distributions and weighted means from compact materialized data; snap polling windows to hours, preserve missing/invalid/legacy sample semantics, and measure refresh/storage costs.
- [x] Server #159: materialize path classification, share window parsing, guard database-derived array indexes and retain all 256 decoder-header checks.
- [x] Web #60: shared map-location validation in independent #61 omits reset/invalid markers and links while preserving valid zero-axis locations and stored records. Native and real-data browser checks pass.
- [x] Web #58: distinct navigation glyphs in #59, plus dedicated RF/Signal and Paths glyphs in #55/#57.
- [x] Refresh #55/#57 after the accepted #52/#53 squash. Their source trees were identical after the September 20 refresh; that history-only update needs no replacement Pi artifact.
- [x] All eight application PRs pass their required checks on the published heads. Native PostgreSQL tests ran. The upstream web CodeQL job remains skipped under its existing policy and is not counted as a scan.

These checkmarks record completed corrections and validation, not maintainer approval. The four server PRs, four web PRs and docs #5 still await their merge/review decisions.

Review order is server #149 -> #154 -> #157 -> #159. Web #55 waits for #157 to be merged **and deployed**; #57 waits for #159 to be merged and deployed and for #55. The icon fix can be reviewed independently. Traffic and Scopes have already landed together as web e01c090; do not replay #52.

## Storage and retention boundary

The September 17 drop-and-reset observation-partitioning design and implementation plan were explicitly superseded on September 19. They are historical reference only. Do not implement their table drop, history reset or process-local dedup replacement.

The stated replacement direction is lz4 compression, batched deletes, per-table autovacuum tuning and a seven-day default. Those changes are not present in the verified published server dev 951b79b (its example still says 30 days). Obtain and review the replacement contribution before describing it as shipped. Coordinate append-only migration numbers with that work; the old plan's proposed 035 is not evidence that a migration exists.

A consolidation release must document its actual retention behavior and capacity limits. A future production parity cutover also needs verified durable history coverage and recovery copies. Do not infer either from example configuration or the Pi's short history.

## Combined-candidate evidence

- [x] Native Pi build/test of server `6be0f762` and web `42ba5fc`, including real PostgreSQL-to-HTTP checks and migration retry/concurrent refresh; 786 web tests pass.
- [x] One-million-row request/initial-population/refresh/storage measurements; request plans read only the new views. Signal: 1.8–77.5 ms reads, 14.4 s initial population, 16.8 s refresh, 6.5 MB. Paths: 3.5–141.9 ms reads, 8.4 s population, 6.2 s refresh, 11.3 MB.
- [ ] Measure the full operator workload and sustained refresh/ingest load before a production parity claim. The million-row fixture does not establish that limit.
- [x] Backup client mismatch and unsupported-DSN cases leave the public API available; valid client export/restore used disposable data only and restored all 35 source migrations. Public preview admin/backup remains disabled.
- [x] Real preview analytics reconcile with SQL for the materialized window. Browser charts, complete-hour text, small screens and error/empty/retry states are verified. Both MQTT feeds advance and the public browser reports LIVE.
- [x] Current and rollback server/web artifacts, exact source offers and visible changelog match the running pair. Only the Beacon app restarted; the other 20 containers were preserved. Additive rollup migrations retain observations and are compatible with the previous binary.

The immediate server rollback from the packet-reference update is `6be0f762` with current web `42ba5fcb`. The previous frontend rollback `19672038` and earlier full pair, server `4f6679c8` / web `b1100972`, are also retained. The local deployment record preserves binaries, assets, source archives and runners. Rolling back the application keeps the additive rollup views; it does not remove history.

## Maintainer release handoff

1. Merge the reviewed queue in the declared order, using the shared refresh helper after accepted parents. Do not manually rebase every PR from scratch.
2. Deploy the accepted server before merging/deploying pages that need its new endpoints. Verify endpoint availability on the intended deployment, not just the Pi preview.
3. Freeze exact reviewed server/web dev heads and rerun required checks on them. Refresh the release notes with only changes actually included.
4. Follow the server contribution guide for a signed version/Swagger commit, dev-to-main fast-forward, tag and release CI. Web main has a prior release squash (`5ac36ce`) outside dev ancestry; maintainers must reconcile that stable history before choosing its promotion method. Do not silently overwrite main.
5. Verify the tag's Actions-built artifacts and matching source. Publish accurate release notes, upgrade/retention guidance, known gaps and rollback instructions.
6. After both releases, empty the accepted review queues and start the next feature directly from freshly fetched dev. Resume the parity roadmap; this milestone does not close partial #60/#72, #99, #116 or internationalization #12.
