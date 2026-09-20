# Beacon parity and analytics roadmap

Updated 20 September 2026. This is the working roadmap for n30nex's ongoing contributions toward CoreScope feature parity. Maintainers decide acceptance and merge order; deployment owners handle the production switch.

Refresh GitHub issues, PR feedback and branch state before starting a phase. This document is a snapshot, and linked issues/PRs are the current source of truth.

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

## Current review queue

All active contribution PRs are available for review without draft status at the contributor's request. Dependencies still determine merge order. Review requests do not establish approval, and required checks must pass on the current published head.

Server order: **#149 → #154 → #157 → #159**.

| PR | Scope | Issue disposition |
|---|---|---|
| [Server #149](https://github.com/MeshCore-Beacon/beacon-server/pull/149) | Protected operator-account lifecycle | Partial #60; these records are not browser logins |
| [Server #154](https://github.com/MeshCore-Beacon/beacon-server/pull/154) | Protected database/config backup download | Partial #72; login, validation/import and deployment-file coverage remain |
| [Server #157](https://github.com/MeshCore-Beacon/beacon-server/pull/157) | Bounded SNR/RSSI distributions and hourly statistics | Complete endpoint scope in #156 |
| [Server #159](https://github.com/MeshCore-Beacon/beacon-server/pull/159) | Bounded received-path and hash-width statistics | Complete endpoint scope in #158 |
| [Server #160](https://github.com/MeshCore-Beacon/beacon-server/pull/160) | Offline, non-destructive backup archive verification | Independent accepted-dev parent `951b79b`; partial #72, outside the shared stack |
| [Server #161](https://github.com/MeshCore-Beacon/beacon-server/pull/161) | ACK identifiers and TRACE/PING tags in packet summaries | Independent accepted-dev parent `951b79b`; partial #99, clean overlay on the shared stack |

#160 is an independent CLI follow-up and does not block the consolidation release. Candidate `262eae96` passes Windows/native Pi build, format, vet and unit checks, Windows race checks, malformed-input/fuzz cases, and exact compiled PostgreSQL export/verify/restore; CI/CodeQL pass. The Pi race runtime cannot initialize on its kernel and is recorded as unavailable. The CLI remains installed separately, with its own source link on the preview changelog. The validator checks archive structure and integrity, not authenticity, safe SQL or restorability.

#161 at `0befdc5c` also remains independent. Native builds of the standalone and combined candidates pass, including 28 PostgreSQL fixtures that keep each global/regional/backfill read to one query; Windows ingest race checks and CI/CodeQL pass. Public historical summaries and a live PING match packet detail, with 1280px/390px browser checks and no horizontal overflow. The existing web renders the new text without a client release. References are packet-carried checksums/tags, not identities or delivery/authentication guarantees. No message body or trace auth code is added. This follow-up does not block the consolidation release.

Web order: **#59 → #55 → #57**, with independent map correction **#61** also ready. The icon correction #59 can land independently; #55/#57 wait until their server endpoints are merged and deployed. Traffic #52 landed verbatim in the #53 squash (`e01c090`); #52 was closed as included, and #53 is merged. Issues #50/#51 are closed. Observer comparison [#48](https://github.com/MeshCore-Beacon/beacon-web/pull/48) and foreign-node display [#49](https://github.com/MeshCore-Beacon/beacon-web/pull/49) are also merged.

| PR | Scope | Dependency / issue |
|---|---|---|
| [Web #52](https://github.com/MeshCore-Beacon/beacon-web/pull/52) | Traffic heatmap, hourly trends and reception share | Included in merged #53; #50 closed |
| [Web #53](https://github.com/MeshCore-Beacon/beacon-web/pull/53) | Regional scope charts and exact counts | Merged as e01c090; #51 closed |
| [Web #61](https://github.com/MeshCore-Beacon/beacon-web/pull/61) | Omit reset/invalid map locations and false neighbour/path lines | Independent correction; #60 |
| [Web #59](https://github.com/MeshCore-Beacon/beacon-web/pull/59) | Distinct Traffic, Scopes and Compare icons | Independent correction; #58 |
| [Web #55](https://github.com/MeshCore-Beacon/beacon-web/pull/55) | RF / Signal charts and sample availability | After #59 and server #157 is merged and deployed; #54 |
| [Web #57](https://github.com/MeshCore-Beacon/beacon-web/pull/57) | Paths & Hashes charts and classification coverage | After #55 and server #159 is merged and deployed; #56 |

The router foundation [server #155](https://github.com/MeshCore-Beacon/beacon-server/pull/155) is merged. The refresh workflow drops accepted squash parents, preserves focused feature deltas and handles changed branch history in isolated worktrees. See [the executable contributor workflow](CONTRIBUTOR_WORKFLOW.md).

## Delivered foundations

- Faster bounded node, route, trace and clock-stat queries; list-limit validation and NULL-observation handling. Representative changes: [#111](https://github.com/MeshCore-Beacon/beacon-server/pull/111), [#118](https://github.com/MeshCore-Beacon/beacon-server/pull/118), [#120](https://github.com/MeshCore-Beacon/beacon-server/pull/120), [#122](https://github.com/MeshCore-Beacon/beacon-server/pull/122), [#124](https://github.com/MeshCore-Beacon/beacon-server/pull/124).
- MQTT client isolation, proxy identity handling, API/WebSocket limits and interrupted-index recovery. Timeout attribution in #116 remains separate from these accepted fixes.
- Observer age-out, advert summaries, endpoint snapshots and companion matching, stable channel paging, packet search and shared packet links.
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

The current combined preview has passed native Go/PostgreSQL/HTTP validation and **786 web tests**. Private backup checks cover version compatibility, feature-only startup failure, TLS/password files, cancellation and schema/data/sequence restoration. The review update passed 390/1280px browser checks, with ten distinct glyphs and explicit complete-hour text; earlier chart validation also covered 320/768px. Public Signal/Paths counts reconcile with SQL, both MQTT feeds advance and the browser reports LIVE. Current revisions and corresponding-source archives are on the preview's changelog page.

The current Pi build is server `5848d200` with unchanged web `42ba5fcb`. It composes #161 with the reviewed server stack; no existing PR branch was rewritten. Both MQTT feeds advance, schema/config remain unchanged and the other 20 containers were preserved. Packet-reference reads took 4.39–22.83 ms at the origin. The map correction and separate backup-verifier tool remain included. Current/rollback source and binaries are retained; only verified inactive staging was retired.

## Next phases

The September 20 #116 investigation has a new [current-build result](https://github.com/MeshCore-Beacon/beacon-server/issues/116#issuecomment-5753626821): a 600-second unmodified Pi capture kept both feeds connected and retained 2,169 new observations, with no ping timeout, disconnect, deadline, SQLSTATE error or HTTP 5xx response. App/PostgreSQL CPU averaged 2.14%/3.96% of one core. The preceding 3h39 log likewise has no MQTT loss or deadline error. Timestamp warnings were classified separately. This did not measure callback or pool-acquisition duration and does not establish the original cause or production capacity. No application, ordering, acknowledgement or service change was made; #116 remains open. Further capture should follow a recurrence or meaningful workload change, rather than repeatedly sampling the same healthy state.

1. **Finish the current queue and prepare a consolidation release.** Address all four server reviews and the analytics icon regression [web #58](https://github.com/MeshCore-Beacon/beacon-web/issues/58). Validate the combined candidate on the Pi, retain backend-before-frontend deployment order, then hand reviewed `dev` candidates to maintainers for the server/web main releases. Follow [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md). Pause new analytics until this breakpoint; this release does not claim complete CoreScope parity.
2. **After the consolidation release: Channel Activity analytics.** Inspect existing aggregates and add bounded channel traffic/trend views. Define messages versus receptions, unknown/encrypted-channel coverage and the behavior when keys are unavailable. Keep keys and message contents out of aggregate responses; avoid raw-message paging to build statistics.
3. **Observed ambiguity and topology.** Separate static prefix conflicts from observed unresolved/ambiguous paths. Add justified route-pattern, neighbour, hop and distance views with clear provenance and bounded work.
4. **Administration and backup slices.** Non-destructive archive validation is ready in independent #160. Resolve browser login/session and restore authorization before an import endpoint; keep deployment-file coverage and remote/scheduled backup separate. Test restoration against disposable databases. These follow-ups do not delay the current release.
5. **Production evidence and handoff.** Reconcile history, operational limits and the parity matrix below before preparing a release/cutover handoff.

## Listed work still open

| Issue | Remaining scope |
|---|---|
| [Server #116](https://github.com/MeshCore-Beacon/beacon-server/issues/116) | No recurrence in the September 20 retained log / ten-minute capture; still needs an attributable event with callback/pool timing |
| [Server #99](https://github.com/MeshCore-Beacon/beacon-server/issues/99) | Advert names are accepted; ACK/TRACE/PING references in #161 await review; define any remaining packet-type formats |
| [Server #60](https://github.com/MeshCore-Beacon/beacon-server/issues/60) | Remaining administration/worker/persistence behavior; account records do not establish login sessions |
| [Server #72](https://github.com/MeshCore-Beacon/beacon-server/issues/72) | Archive validation #160 awaits review; import, browser access, deployment-file coverage and remote/scheduled backup remain |
| [Web #12](https://github.com/MeshCore-Beacon/beacon-web/issues/12) | Supported-language and formatting scope for internationalization |
| [Web #60](https://github.com/MeshCore-Beacon/beacon-web/issues/60) | Map location-reset correction #61 is deployed and awaiting merge |
| [Web #58](https://github.com/MeshCore-Beacon/beacon-web/issues/58) | Distinct analytics navigation icons, including pending RF/Signal and Paths pages |

The analytics endpoint/page issues remain open while their corresponding PRs await merge. Use closing references only when a PR completes the issue's accepted scope; use related references for partial work.

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
