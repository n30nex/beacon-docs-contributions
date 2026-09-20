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

Web order: **#52 → #53 → #55 → #57**. Observer comparison [#48](https://github.com/MeshCore-Beacon/beacon-web/pull/48) and foreign-node display [#49](https://github.com/MeshCore-Beacon/beacon-web/pull/49) are merged; issue #26 is closed.

| PR | Scope | Dependency / issue |
|---|---|---|
| [Web #52](https://github.com/MeshCore-Beacon/beacon-web/pull/52) | Traffic heatmap, hourly trends and reception share | #50 |
| [Web #53](https://github.com/MeshCore-Beacon/beacon-web/pull/53) | Regional scope charts and exact counts | After #52; #51 |
| [Web #55](https://github.com/MeshCore-Beacon/beacon-web/pull/55) | RF / Signal charts and sample availability | After #53 and server #157; #54 |
| [Web #57](https://github.com/MeshCore-Beacon/beacon-web/pull/57) | Paths & Hashes charts and classification coverage | After #55 and server #159; #56 |

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

Both new aggregate APIs accept explicit windows of at most 30 days, propagate cancellation, use region-specific caching and have a 15-second execution bound. A raw 30-day global query can still take seconds at larger volumes. On a shared Pi with one million synthetic rows, signal queries measured about 2.1–6.5 seconds and path queries 2.8–7.5 seconds across prepared-plan modes. Measure production volume before choosing precomputed distributions or claiming release readiness.

The current combined preview has passed native Go/PostgreSQL/HTTP validation and **781 web tests**, plus desktop/mobile layout checks at 320/390/768/1280px. Synthetic fixtures tested gaps, trace/unclassified data, zero samples, errors/retry and long windows; they were not published. Current revisions and corresponding-source archives are on the preview's changelog page.

## Next phases

1. **Review feedback and regressions first.** Refresh both application queues, resolve attributable failures, and retain explicit issue scope.
2. **Channel Activity analytics.** Inspect existing aggregates and add bounded channel traffic/trend views. Define messages versus receptions, unknown/encrypted-channel coverage and the behavior when keys are unavailable. Keep keys and message contents out of aggregate responses; avoid raw-message paging to build statistics.
3. **Observed ambiguity and topology.** Separate static prefix conflicts from observed unresolved/ambiguous paths. Add justified route-pattern, neighbour, hop and distance views with clear provenance and bounded work.
4. **Queued administration and backup slices.** Add non-destructive archive validation, then resolve browser login/session, import and deployment-file coverage separately. Test restoration against disposable databases.
5. **Production evidence and handoff.** Reconcile history, operational limits and the parity matrix below before preparing a release/cutover handoff.

## Listed work still open

| Issue | Remaining scope |
|---|---|
| [Server #116](https://github.com/MeshCore-Beacon/beacon-server/issues/116) | Attribute repeated MQTT ping timeouts to a measured cause; fresh traffic alone is insufficient |
| [Server #99](https://github.com/MeshCore-Beacon/beacon-server/issues/99) | Define and complete remaining packet-type summary coverage after advert summaries |
| [Server #60](https://github.com/MeshCore-Beacon/beacon-server/issues/60) | Remaining administration/worker/persistence behavior; account records do not establish login sessions |
| [Server #72](https://github.com/MeshCore-Beacon/beacon-server/issues/72) | Archive validation/import, browser access, deployment-file coverage and remote/scheduled backup scope |
| [Web #12](https://github.com/MeshCore-Beacon/beacon-web/issues/12) | Supported-language and formatting scope for internationalization |

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
