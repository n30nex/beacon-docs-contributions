# Server/web consolidation release

Status: accepted-dev validation and release handoff, 24 September 2026. All ten application/CLI PRs in the consolidation batch are merged. Stable tags remain unchanged; this is not a published release or a full CoreScope parity claim.

## Scope and stop point

Release the accepted account/backup/analytics batch before Channel Activity or further parity expansion. Current public tags are server v1.6.0 and web v1.3.0; maintainers choose the next versions and perform signed release commits, main promotion and tags under each repository's contribution rules.

The deployment owner performs the eventual CoreScope switch. Beacon remains at dev.meshcore.ca, CoreScope at live.meshcore.ca, and the Pi preview remains at canadaverse.org/beacon-dev/ with its changelog and corresponding source.

The release candidate includes both formerly independent follow-ups: [server #160](https://github.com/MeshCore-Beacon/beacon-server/pull/160) for offline archive verification and [server #161](https://github.com/MeshCore-Beacon/beacon-server/pull/161) for ACK/TRACE/PING summaries. Their wider issues #72 and #99 remain partial. Integrity checks do not establish archive authenticity or restorability; packet references do not establish identity or delivery.

Accepted server: `c02317a4ac7228d19cab498edfa1d61186c84626`.
Accepted web: `0f0a6ca51c7b2c3315db77954f61b30bbdeea5e2`.
The web source tree is identical to tested preview `42ba5fcb`; preserve that artifact's actual revision/source instead of relabeling it. The server differs from preview `5848d200` only in the verifier CLI/library/tests/docs; its verifier code and tests are identical to separately tested `262eae96`. The documentation additionally contains the accepted protected-download section.

## Review gates

- [x] Workflow checks include every independent preview PR, not just the ordered stack. Status reports them; Check verifies their CI and source; Refresh/Publish reject changed prepared inputs. Server #161 and web #61 are covered by the normal preview checks. The standalone backup CLI #160 is checked with its separate manifest.
- [x] Server #149: document POST/DELETE browser preflights and the full admin CORS method example. Keep public read-only defaults.
- [x] Server #154: verify pg_dump/server compatibility at startup; an optional backup prerequisite failure disables only backup, with a specific operator diagnostic. Document backup.enabled and distinguish the export size limit. Native testing caught and fixed the text-versus-integer version-setting scan; CI now covers it with PostgreSQL.
- [x] Server #157: serve Signal distributions and weighted means from compact materialized data; snap polling windows to hours, preserve missing/invalid/legacy sample semantics, and measure refresh/storage costs.
- [x] Server #159: materialize path classification, share window parsing, guard database-derived array indexes and retain all 256 decoder-header checks.
- [x] Web #60: shared map-location validation in independent #61 omits reset/invalid markers and links while preserving valid zero-axis locations and stored records. Native and real-data browser checks pass.
- [x] Web #58: distinct navigation glyphs in #59, plus dedicated RF/Signal and Paths glyphs in #55/#57.
- [x] Refresh #55/#57 after the accepted #52/#53 squash. Their source trees were identical after the September 20 refresh; that history-only update needs no replacement Pi artifact.
- [x] All eight application PRs pass their required checks on the published heads. Native PostgreSQL tests ran. The upstream web CodeQL job remains skipped under its existing policy and is not counted as a scan.

All six server PRs and four web PRs have merged. Server #156/#158 and web #54/#56/#58/#60 are closed. Docs #5 remains open; language foundation #62 has since merged, and translations #63/#64/#65/#66/#69/#70 and independent bug fixes #68/#72 remain outside this original frozen batch. The helper retired accepted parents/overlays without rebasing or force-pushing any application branch. Future work starts from freshly fetched dev. Backend endpoints still need deployment before dependent pages on each operator's target; Pi evidence is not evidence of another deployment.

## Storage and retention boundary

The September 17 drop-and-reset observation-partitioning design and implementation plan were explicitly superseded on September 19. They are historical reference only. Do not implement their table drop, history reset or process-local dedup replacement.

The stated replacement direction is lz4 compression, batched deletes, per-table autovacuum tuning and a seven-day default. Those changes are not present in the verified published server dev c02317a4 (its example still says 30 days). Obtain and review the replacement contribution before describing it as shipped. Coordinate append-only migration numbers with that work; the old plan's proposed 035 is not evidence that a migration exists.

A consolidation release must document its actual retention behavior and capacity limits. A future production parity cutover also needs verified durable history coverage and recovery copies. Do not infer either from example configuration or the Pi's short history.

Language foundation #62 has since merged as accepted web dev `6d3edbb6`, source-equivalent to tested build `1c77f200`. The live preview combines translations through #70 with independent #68/#72 at `9d96b943`: native Pi build/lint and 867 tests pass, with public/browser/source checks. Independent Mesh #72 passes 809 Windows tests/CI and Talkers #68 retains its 808-test evidence; either can merge first to close #71/#67. Immediate frontend rollback is combined `300ee974`. The real scope dataset is empty; physical Safari remains untested. The original release freeze stays separate; maintainers choose whether to advance it to these later contributions.

## Accepted-dev verification - 24 September

- [x] Exact dev CI/image builds pass at server `c02317a4` and web `0f0a6ca5`; server CodeQL/coverage pass and web CodeQL remains skipped.
- [x] Server `c02317a4` built/tested natively on the Pi with real PostgreSQL: 1,194 passing test/subtest results. Signal, Paths, observer comparison, migration recovery, packet summaries and NULL observations ran. Two opt-in backup export/download integration suites were skipped; prior private restore/TLS checks remain separately dated evidence.
- [x] Accepted server is running on the preview. Source/asset hashes match; both feeds advance. Signal/Paths reconcile with SQL for global/regional 1/7/30-day selections, at 2-19 ms origin latency. Only three complete hours are populated; this does not prove 7/30-day history coverage.
- [x] Browser Signal/Paths charts and map load with LIVE status and no captured warnings/errors. Unchanged frontend assets keep their actual `42ba5fcb` build/source identity and prior 786-test evidence; accepted `0f0a6ca5` has the identical tree.
- [x] Only the Beacon app restarted; the other 22 containers and configuration/migration journal were preserved. Immediate rollback is server `5848d200` with unchanged web. The separate verifier retains its real `262eae96` binary/source identity.
- [x] Accepted review queues/overlays were retired. Start created the independent language branch directly from accepted dev; #63 followed by #64, #65, #66, #69 and #70 is the translation queue, with #68/#72 independently included in preview checks. Completed issues are closed; five broader issues and focused #67/#71 remain open.
- [ ] Maintainer version selection, signed release commits, main promotion, tags and tag-built artifact verification. Stable releases remain v1.6.0 / v1.3.0.

## Earlier combined-candidate evidence - 20 September

- [x] September 20 unmodified Pi stability sample: 600 seconds / 41 samples, both feeds connected, 2,169 retained observations and no MQTT disconnect/deadline or HTTP 5xx. App/PostgreSQL CPU averaged 2.14%/3.96% of one core. This is a bounded health sample, not callback timing, #116 root-cause proof or a production-volume gate. [Result and limits](https://github.com/MeshCore-Beacon/beacon-server/issues/116#issuecomment-5753626821).
- [x] Native Pi build/test of server `6be0f762` and web `42ba5fc`, including real PostgreSQL-to-HTTP checks and migration retry/concurrent refresh; 786 web tests pass.
- [x] One-million-row request/initial-population/refresh/storage measurements; request plans read only the new views. Signal: 1.8–77.5 ms reads, 14.4 s initial population, 16.8 s refresh, 6.5 MB. Paths: 3.5–141.9 ms reads, 8.4 s population, 6.2 s refresh, 11.3 MB.
- [ ] Measure the full operator workload and sustained refresh/ingest load before a production parity claim. The million-row fixture does not establish that limit.
- [x] Backup client mismatch and unsupported-DSN cases leave the public API available; valid client export/restore used disposable data only and restored all 35 source migrations. Public preview admin/backup remains disabled.
- [x] Real preview analytics reconcile with SQL for the materialized window. Browser charts, complete-hour text, small screens and error/empty/retry states are verified. Both MQTT feeds advance and the public browser reports LIVE.
- [x] Current and rollback server/web artifacts, exact source offers and visible changelog match the running pair. Only the Beacon app restarted; the other 20 containers were preserved. Additive rollup migrations retain observations and are compatible with the previous binary.

The current immediate rollback restores combined frontend `300ee974` with server `c02317a4`. Restore accepted frontend `42ba5fcb` before using the older consolidation server rollback to `5848d200`; its metadata describes the accepted frontend. The September 20 packet-reference rollback to `6be0f762` is an older recovery point. Exact artifacts/runners are retained; application rollback keeps additive rollup views and does not remove history.

## Maintainer release handoff

1. The application review queue is accepted. Freeze server `c02317a4` / web `0f0a6ca5`, or explicitly record any newer accepted changes before release. Confirm required checks on those exact heads.
2. Deploy the accepted server before dependent pages and verify both endpoints on the intended deployment. The Pi is a development validation target; production cutover remains with the owner.
3. Follow the server contribution guide for a signed version/Swagger commit, dev-to-main fast-forward, tag and release CI. Web main has the prior release squash `5ac36ce` outside dev ancestry; reconcile that stable history before promotion. Do not overwrite main.
4. Verify the tag's Actions-built artifacts and matching source. Publish accurate notes, upgrade/retention guidance, known gaps and rollback instructions. Versions/tags have not been chosen by this contribution.
5. Review the seven open issues first when resuming development: server #60/#72/#99/#116 and web #12/#67/#71. Independent web #68/#72 close the two focused bugs on acceptance; the other issues remain partial. After the consolidation release, Channel Activity is the next analytics page; this milestone does not establish full CoreScope parity.
