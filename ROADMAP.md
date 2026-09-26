# Beacon parity and analytics roadmap

Updated 26 September 2026 UTC. This is the working roadmap for n30nex's ongoing contributions toward CoreScope feature parity. Maintainers decide acceptance and merge order; deployment owners handle the production switch.

Refresh GitHub issues, PR feedback and branch state before starting a phase. This document is a snapshot, and linked issues/PRs are the current source of truth.

Release-check correction, 21 September UTC: the workflow now includes independent preview PRs in Status and Check, applies the same CI/head/fork/target requirements to them, and rechecks the prepared independent inputs before publication. This covers packet summaries #161 and map correction #61 without adding them to the ordered stacks. The backup CLI #160 retains its separate check. Twenty-three offline regressions cover these gates and the existing no-rebase/cache behavior. See [the contributor workflow](CONTRIBUTOR_WORKFLOW.md).

## Direction

Bring useful CoreScope investigation and analytics features into Beacon's existing ingest, database, API, cache and web components. Prioritize review regressions and measured stability/performance problems, then useful analytics pages. Keep each API or page a focused contribution with explicit counting semantics and validation.

Current sites:

- [Beacon reference deployment](https://dev.meshcore.ca/)
- [CoreScope reference deployment](https://live.meshcore.ca/)
- [Development preview](https://canadaverse.org/beacon-dev/) and its [changelog/source](https://canadaverse.org/beacon-dev/source.html)

| Repository | Responsibility | Contribution target |
|---|---|---|
| [beacon-server](https://github.com/MeshCore-Beacon/beacon-server) | Ingest, storage, read models and public/protected APIs | `dev` |
| [beacon-web](https://github.com/MeshCore-Beacon/beacon-web) | Investigation tools and analytics pages | `dev` |
| [beacon-docs](https://github.com/MeshCore-Beacon/beacon-docs) | Shared contracts, operator guidance and this roadmap | `main` |
| [beacon-mobile](https://github.com/MeshCore-Beacon/beacon-mobile) | Mobile client; coordinate API compatibility | `main` |

## Accepted consolidation batch

All ten original server/web contributions merged on September 24. The September 25 web batch is also accepted: #70 contains translations #63/#64/#65/#66/#69 plus Timestamp wording; #68 and #72 merged separately and closed #67/#71. The five earlier translation PRs were closed as included, with exact ancestry/tree equivalence verified. Web #73 and server #162/#163 then landed. That acceptance batch cleared the application queue. The new September 26 retention/endpoint PRs and docs #5 are now in review, as listed below.

Current accepted dev is server `91b4b457b5f233e9b90b4030e30623095e950714` / web `54b5093ac0302c7db9d51e1d7fe23570eae7cdb5`. Exact-head CI/image builds pass; server coverage/CodeQL pass and web CodeQL remains skipped. Stable releases are still server **v1.6.0** and web **v1.3.0**. The original September 24 freeze (`c02317a4` / `0f0a6ca5`) remains historical evidence, not proof that the newer server migrations are Pi-validated.

| Accepted PR | Scope | Merge commit |
|---|---|---|
| [Server #149](https://github.com/MeshCore-Beacon/beacon-server/pull/149) | add protected account lifecycle endpoints | `4d2642ab` |
| [Server #154](https://github.com/MeshCore-Beacon/beacon-server/pull/154) | add protected database and config download | `a25e2675` |
| [Server #157](https://github.com/MeshCore-Beacon/beacon-server/pull/157) | add bounded reception signal analytics | `6107578c` |
| [Server #159](https://github.com/MeshCore-Beacon/beacon-server/pull/159) | add bounded path and hash-width analytics | `8a3fa7e6` |
| [Server #160](https://github.com/MeshCore-Beacon/beacon-server/pull/160) | verify native archives offline without extraction | `20691dc5` |
| [Server #161](https://github.com/MeshCore-Beacon/beacon-server/pull/161) | summarize ACK and trace references | `c02317a4` |
| [Web #55](https://github.com/MeshCore-Beacon/beacon-web/pull/55) | add RF and signal analytics | `2405e1ac` |
| [Web #57](https://github.com/MeshCore-Beacon/beacon-web/pull/57) | add Paths and Hashes analytics | `929ba83c` |
| [Web #59](https://github.com/MeshCore-Beacon/beacon-web/pull/59) | distinguish analytics navigation icons | `c2ab29a5` |
| [Web #61](https://github.com/MeshCore-Beacon/beacon-web/pull/61) | omit reset and invalid node locations | `0f0a6ca5` |

Server #156/#158 and web #54/#56/#58/#60 are closed. Server #60/#72/#99/#116 and web #12 remain open for their remaining scope. Web #67/#71 are closed following #68/#72. Archive verification establishes structure and integrity, not authenticity, SQL safety or restorability. Packet-carried ACK/TRACE/PING references are not identity or delivery guarantees.

## September 26 retention and endpoint fixes

The Pi was first matched to accepted dev server `91b4b457` / web `54b5093a`, including native validation and a verified restore across migrations 037/038. It now runs composed server `a8394f10` and web `3a18e6d1`, adding three focused review candidates:

| PR | Head | Scope / closure |
|---|---|---|
| [Server #166](https://github.com/MeshCore-Beacon/beacon-server/pull/166) | `74f16de8` | First/renamed adverts resolve after the node update; closes #164 |
| [Server #167](https://github.com/MeshCore-Beacon/beacon-server/pull/167) | `76428b1b` | 30-day hourly summaries survive raw packet expiry; closes #165 |
| [Web #75](https://github.com/MeshCore-Beacon/beacon-web/pull/75) | `3a18e6d1` | Additional-match count and all endpoint candidates on hover, keyboard or touch; closes #74 |

All are out of draft. Exact-head build CI passes, server CodeQL passes, and web CodeQL remains skipped. MrAlders0n/Claude review was requested in PR comments because formal review requests are unavailable to the contributor account. Both server PRs are independent on the same accepted dev and may merge in either order. Web #75 is also independent. The workflow records #167 plus #166 as a complete PR/head preview input; its separate manifest can be refreshed after upstream changes. No routine manual restacking is required for these non-overlapping changes. No upstream PR was merged by the contributor.

The agreed Pi policy is **72-hour raw packets, 30-day hourly analytics and 720-hour telemetry**. Migration 039 archives compact summaries as each raw packet cohort expires, atomically with deletion, without storing bodies or raw paths. Traffic, payload, top observers, talkers, advertisers, observer activity, Signal and Paths use the retained summaries. Already-purged history cannot be recovered. Packet detail, sub-hour activity and exact observer comparisons still use retained raw data; entity/scope/radio population counts keep their current meaning.

Full Windows and native Pi Go/PostgreSQL checks pass, including rollback on archive failure, retries, concurrent ingestion, late observations, distinct observers across batches, multiple IATAs, nullable/radio/path semantics and independent 30-day expiry. The full frontend build/lint and **874 tests** pass. A 1,001-packet fixture with 1KB bodies compacted to at most twelve archive rows; the first Pi run took 85ms for archive/deletion, which is a fixture measurement rather than a production-throughput guarantee. A restored copy of the actual preview database retained all eight view counts after every raw packet was deleted in a rolled-back test. Source/index hashes and the public candidate popup were verified.

Migration 039 preserved fingerprints of all 23 original application tables. The actual prior schema038 database, exact binary/configuration and private dump remain available for rollback; older pre-038 recovery is retained separately. Only the Beacon preview app restarted (about 33 seconds); 22 other containers were unchanged and both MQTT feeds reconnected. Public admin/backup and foreign detection remain disabled. [Current changelog and corresponding source](https://canadaverse.org/beacon-dev/source.html).

Current broader issues remain server #60 (admin), #72 (backup/import), #99 (packet summaries), #116 (MQTT investigation), and web #12 (remaining translations). Prioritize feedback and acceptance of these new fixes, then a focused Mesh/Talkers/Observer translation slice under #12. A measured month of accumulated history, production-scale capacity and physical Safari checks remain separate gates. Maintainers own stable releases and the owners handle production cutover.

## Delivered foundations

- Faster bounded node, route, trace and clock-stat queries; list-limit validation and NULL-observation handling. Representative changes: [#111](https://github.com/MeshCore-Beacon/beacon-server/pull/111), [#118](https://github.com/MeshCore-Beacon/beacon-server/pull/118), [#120](https://github.com/MeshCore-Beacon/beacon-server/pull/120), [#122](https://github.com/MeshCore-Beacon/beacon-server/pull/122), [#124](https://github.com/MeshCore-Beacon/beacon-server/pull/124).
- MQTT client isolation, proxy identity handling, API/WebSocket limits and interrupted-index recovery. Timeout attribution in #116 remains separate from these accepted fixes.
- Observer age-out, advert summaries, batched endpoint resolution and companion matching (snapshots superseded by #163), stable channel paging, packet search and shared packet links.
- Observer activity/telemetry and comparison, regional scope statistics, runtime administration, optional foreign-repeater detection and the backup-export foundation.

## Analytics delivery and counting rules

| Page | Current behavior | Important interpretation |
|---|---|---|
| [Traffic](https://canadaverse.org/beacon-dev/?tab=Analytics&statsTab=traffic&range=24h) | UTC hourly heatmap, IATA trends, reception share and exact counts | Counts reported receptions; missing hourly records remain gaps |
| [Scopes](https://canadaverse.org/beacon-dev/?tab=Analytics&statsTab=scopes) | Regional packet, observer-membership and default-scope-node charts | Retained counts have no rolling date filter; memberships can overlap |
| [RF / Signal](https://canadaverse.org/beacon-dev/?tab=Analytics&statsTab=signal&range=24h) | SNR/RSSI distributions, hourly means, sample coverage and exact tables | Missing/non-finite and unavailable zero/zero readings are excluded per metric; a measured zero SNR remains valid |
| [Paths & Hashes](https://canadaverse.org/beacon-dev/?tab=Analytics&statsTab=paths&range=24h) | Hash-width share, received header-entry distribution, hourly trends and coverage | Empty paths never vote for width; TRACE paths hold signal readings; unusable metadata is unclassified |

The path page counts stored receptions, not unique devices. Flood paths accumulate entries, while direct routes carry remaining entries. Observed widths do not establish device capability or collision rates. Signal readings describe reception at the reporting observer rather than a complete end-to-end link.

The September 20 review correction moves both new aggregate APIs onto materialized hourly snapshots, preserving reception/region semantics and normalizing polling windows to UTC hours. In a rolled-back million-row Pi fixture, Signal request queries took 1.8–77.5 ms and Paths 3.5–141.9 ms across custom/generic plans. Initial population took 14.4/8.4 seconds, refresh 16.8/6.2 seconds, and view/index storage was 6.5/11.3 MB respectively. These measurements cover the fixture, not the full production workload. See the [release consolidation checklist](RELEASE-CHECKLIST.md) for remaining gates.

September 20 validation covered native Go/PostgreSQL/HTTP behavior and **786 web tests**, plus private backup compatibility, feature-only startup failure, TLS/password files, cancellation and schema/data/sequence restoration. That review update passed 390/1280px browser checks, with ten distinct glyphs and complete-hour text; earlier chart checks also covered 320/768px. This is historical evidence for the unchanged feature code. Current revisions and corresponding-source archives are on the preview's changelog page.

The September 24 consolidation check built accepted server `c02317a4` and retained web `42ba5fcb`, identical in source to accepted `0f0a6ca5`. Its native PostgreSQL and public/browser evidence remains in the release checklist. The Pi frontend contains the now-accepted translations and #68/#72 as documented above; the prior combined preview is retained for rollback. The three-hour retained analytics sample does not establish 7/30-day history or production capacity.

## Next phases

The September 20 #116 investigation has a new [current-build result](https://github.com/MeshCore-Beacon/beacon-server/issues/116#issuecomment-5753626821): a 600-second unmodified Pi capture kept both feeds connected and retained 2,169 new observations, with no ping timeout, disconnect, deadline, SQLSTATE error or HTTP 5xx response. App/PostgreSQL CPU averaged 2.14%/3.96% of one core. The preceding 3h39 log likewise has no MQTT loss or deadline error. Timestamp warnings were classified separately. This did not measure callback or pool-acquisition duration and does not establish the original cause or production capacity. No application, ordering, acknowledgement or service change was made; #116 remains open. Further capture should follow a recurrence or meaningful workload change, rather than repeatedly sampling the same healthy state.

1. **Review the retention/endpoint fixes, then publish coordinated releases.** Accepted dev including #162/#163/#73 is now Pi-validated; #166/#167/#75 are independent review candidates on that baseline. Maintainers choose versions, create signed release commits/tags, promote main and verify release artifacts. Follow [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md). Pause new analytics until this breakpoint; this release does not claim complete CoreScope parity.
2. **Continue listed issue #12 in small screen groups.** Foundation, Signal, Paths, Traffic, Scopes, Clock Drift and shared Timestamp work are accepted. Talkers/Mesh fixes are accepted and #67/#71 are closed. After refreshing the Pi, start Mesh, Talkers or Observer analytics translation directly from fresh dev. Preserve measurement/data semantics; broader page, chart, dialog and formatting text remains.

## Listed work still open

| Issue | Remaining scope |
|---|---|
| [Server #116](https://github.com/MeshCore-Beacon/beacon-server/issues/116) | No recurrence in the September 20 retained log / ten-minute capture; still needs an attributable event with callback/pool timing |
| [Server #99](https://github.com/MeshCore-Beacon/beacon-server/issues/99) | Advert names and ACK/TRACE/PING references are accepted; define any remaining packet-type formats |
| [Server #60](https://github.com/MeshCore-Beacon/beacon-server/issues/60) | Remaining administration/worker/persistence behavior; account records do not establish login sessions |
| [Server #72](https://github.com/MeshCore-Beacon/beacon-server/issues/72) | Download #154 and archive validation #160 are accepted; import, browser access, deployment-file coverage and remote/scheduled backup remain |
| [Web #12](https://github.com/MeshCore-Beacon/beacon-web/issues/12) | Foundation and translations through #70 are accepted; Mesh/Talkers fixes are merged. Remaining analytics/screens/dialogs/formatting still need translation |

The six completed analytics/icon/map issues are closed. Refresh the five currently open issues first at every continuation; accepted partial contributions are not grounds to close broader issues. Use closing references only when a PR completes the issue's accepted scope; use related references for partial work.

## Production parity matrix

Matching tab names is not acceptance. Each capability needs verified semantics, time/region behavior, empty/partial data, performance and browser evidence.

| Capability | Coverage / remaining evidence |
|---|---|
| Overview | Mesh overview and Traffic; reconcile packet/reception grain and retained windows |
| RF / Signal | New distributions, weighted means and sample coverage; production-volume measurements remain |
| Topology / route patterns | Existing routes, traces and neighbour graph; deeper edge/subpath/connectivity analysis remains |
| Channels | Directory/chat/talkers exist; traffic statistics, unknown-channel and history behavior remain |
| Hash statistics | Paths & Hashes covers observed ordinary widths and entries; trace-payload widths are distinct |
| Hash issues | Endpoint/path ambiguity primitives exist; observed ambiguity and static conflicts need separate views |
| Node analytics | Existing directory/detail/observations; richer attributed activity, signal, payload and peer analysis remains |
| My Repeaters | Owner selection/watchlist behavior and grouped analytics need an agreed contract |
| Repeater metrics | Observer telemetry overlaps partially; units, resets and role attribution need reconciliation |
| Distance | Coordinates/maps exist; valid link/path distances, unknown positions and confidence remain |
| Neighbour graph | Existing graph needs retained scaling, filter and accessible-fallback acceptance evidence |
| RF health | Noise/airtime/error telemetry exists; comparable health views need real samples and valid deltas |
| Clock health | Existing clock-drift endpoint/UI; retain role, threshold and history semantics |
| Roles | Node-type census exists; activity and unknown-role interpretation need acceptance evidence |
| Scopes | Regional API and new page exist; reconcile against populated retained data |
| Prefix tool | Public-prefix inspection/simulation remains unverified |
| Observer comparison | Merged backend/web; retain distinct-packet, time/region and zero-data tests |
| Other workflows | Validate decoder/search/sharing, live map/replay, settings, optional clients and legacy links |

## Release gates

- Inventory actual CoreScope retention, earliest/latest durable data, configuration and recovery copies. Example retention settings and public in-memory counts are not production history evidence.
- Reconcile Beacon's deduplication, identity, encryption/key and time semantics. Document whether migration or sufficient parallel ingestion supplies each historical window.
- Complete backup recovery scope with private disposable restore tests, including schema/data/sequence continuation and the deliberately excluded deployment files.
- Measure cold start, reconnects, ingest freshness, CPU/memory/storage, query latency and maintenance against representative production volume. Long-window raw aggregates may need rollups.
- Validate keyboard/mobile/browser behavior, chart readability and sharing. Physical iPhone Safari and a sustained load/connection soak remain open validation gaps.
- Verify release artifacts from reviewed source and applicable CI. The upstream web CodeQL workflow is currently disabled; its skipped job does not count as a security scan.
- Publish matching source, configuration guidance, known limitations and a verified rollback procedure. The deployment owner performs the production switch.

The development preview currently has short retained history and no populated transport-scope records. Its public admin/backup and foreign detection are disabled. These limitations remain explicit until configuration and validation support enabling them.

## Keeping this roadmap useful

Update this file when a phase is delivered, a dependency merges, an issue closes or the next priority changes. Keep private configuration and host-specific operational records outside this repository. Link current GitHub work and the public source/changelog so another contributor can continue without a private workstation path.
