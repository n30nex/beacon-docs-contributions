# Beacon parity and analytics roadmap

Updated 25 September 2026 UTC. This is the working roadmap for n30nex's ongoing contributions toward CoreScope feature parity. Maintainers decide acceptance and merge order; deployment owners handle the production switch.

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

All ten server/web contributions merged into `dev` on 24 September UTC. The accepted batch has no remaining rebase dependencies. Language foundation [web #62](https://github.com/MeshCore-Beacon/beacon-web/pull/62) has also merged as `6d3edbb6`. Signal translation [web #63](https://github.com/MeshCore-Beacon/beacon-web/pull/63), Paths translation [web #64](https://github.com/MeshCore-Beacon/beacon-web/pull/64), Traffic translation [web #65](https://github.com/MeshCore-Beacon/beacon-web/pull/65), Scopes translation [web #66](https://github.com/MeshCore-Beacon/beacon-web/pull/66), Clock Drift translation [web #69](https://github.com/MeshCore-Beacon/beacon-web/pull/69), independent Talkers fix [web #68](https://github.com/MeshCore-Beacon/beacon-web/pull/68), and [docs #5](https://github.com/MeshCore-Beacon/beacon-docs/pull/5) remain open.

The original consolidation freeze is server `c02317a4ac7228d19cab498edfa1d61186c84626` / web `0f0a6ca51c7b2c3315db77954f61b30bbdeea5e2`. CI and image builds pass at those heads; web CodeQL remains skipped and is not a security scan. Current web dev has since advanced to `6d3edbb6` through #62. Stable releases are still server **v1.6.0** and web **v1.3.0**. Merged dev is not a published stable release.

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

Server #156/#158 and web #54/#56/#58/#60 are closed. Server #60/#72/#99/#116 and web #12 remain open for their remaining scope. New web #67 has a complete fix in independent #68 awaiting acceptance. Archive verification establishes structure and integrity, not authenticity, SQL safety or restorability. Packet-carried ACK/TRACE/PING references are not identity or delivery guarantees.

The workflow removed the accepted entries and overlays without rebasing or force-pushing any application branch. Signal translation #63 started directly from fresh dev `6d3edbb6`; Paths translation #64 follows its exact `01c6d1aa` head. Traffic translation #65 follows #64 at `3f2a3636`. Scopes #66 follows #65 at `a928fda5`. Clock Drift #69 follows #66 at `8d81bd5d`. Merge #63, #64, #65, #66, then #69. Future overlapping follow-ups use the declared parent through the helper. Preserve actual build identities when accepted commits have identical source trees. See [the contributor workflow](CONTRIBUTOR_WORKFLOW.md) and [consolidation checklist](RELEASE-CHECKLIST.md).

## Current issue work

**Independent correctness fix:** [#68](https://github.com/MeshCore-Beacon/beacon-web/pull/68), `2e3b5161`, remains ready directly on dev and can merge before the translation queue. It closes focused [#67](https://github.com/MeshCore-Beacon/beacon-web/issues/67) on acceptance. The independent source's 808 Windows tests and the prior combined preview's native/browser checks stay separately recorded; Talkers translation follows that same-file fix.

[Clock Drift translation #69](https://github.com/MeshCore-Beacon/beacon-web/pull/69), `efd73757b5eae58c8e9e6b3e01f11cce4603cd85`, follows #66 `8d81bd5d`. **Translation order: #63 -> #64 -> #65 -> #66 -> #69.** It translates the caption, table headings, drift direction words and empty/error labels. Stable column IDs preserve selected sorting and focus as labels change; existing header-based callers remain compatible. Cached pending/error rows use the unavailable state, while healthy background refreshes retain valid data.

The PR source passes Windows build/lint and **847 tests in 96 files**, plus exact-head CI. The actual Pi source `8fb636aafaa303808e6e695f8459d3ac639f9589` also contains independent #68, and passes native build/lint and **853 tests in 97 files**. Signs, units, rounding, warning thresholds, identities/IATAs and regional query keys are preserved. Shared Timestamp formatting and relative “ago” wording remain a later slice.

Local/public browser checks preserve selected node order and signed magnitudes across French switching for 100 live rows, and translated controls restore worst-first sorting. Public French stays EN DIRECT. The 320px layout contains horizontal table scrolling without page overflow. Source/JS/CSS hashes match, both brokers are connected and all 23 containers are unchanged. Initial JS grows by 246 gzip bytes over the previous combined preview. Physical Safari remains untested.

Current Pi: server `c02317a4` / combined web `8fb636aa`. Immediate frontend rollback is `edc32842`, which retains the Talkers fix. Current/rollback artifacts and source remain; completed staging was retired. The [source/changelog](https://canadaverse.org/beacon-dev/source.html) distinguishes PR and combined-build identities. The helper retains independent #68, checks all six application PR heads and reuses validated trees without rewriting existing branches.

Next under #12: shared Timestamp wording while #68 is reviewed, then Talkers translation after its fix lands and one stack refresh. Reuse the stable column IDs from #69 for translated sortable tables. The original consolidation release freeze remains separately owned by the maintainers; history/capacity and physical Safari remain explicit gates.

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

September 20 validation covered native Go/PostgreSQL/HTTP behavior and **786 web tests**, plus private backup compatibility, feature-only startup failure, TLS/password files, cancellation and schema/data/sequence restoration. That review update passed 390/1280px browser checks, with ten distinct glyphs and complete-hour text; earlier chart checks also covered 320/768px. This is historical evidence for the unchanged feature code. Current revisions and corresponding-source archives are on the preview's changelog page.

The September 24 consolidation check built accepted server `c02317a4` and retained web `42ba5fcb`, identical in source to accepted `0f0a6ca5`. Its native PostgreSQL and public/browser evidence remains in the release checklist. The Pi frontend includes #63–#66 and #69 plus independent #68 as documented above; the prior combined preview is retained for rollback. The three-hour retained analytics sample does not establish 7/30-day history or production capacity.

## Next phases

The September 20 #116 investigation has a new [current-build result](https://github.com/MeshCore-Beacon/beacon-server/issues/116#issuecomment-5753626821): a 600-second unmodified Pi capture kept both feeds connected and retained 2,169 new observations, with no ping timeout, disconnect, deadline, SQLSTATE error or HTTP 5xx response. App/PostgreSQL CPU averaged 2.14%/3.96% of one core. The preceding 3h39 log likewise has no MQTT loss or deadline error. Timestamp warnings were classified separately. This did not measure callback or pool-acquisition duration and does not establish the original cause or production capacity. No application, ordering, acknowledgement or service change was made; #116 remains open. Further capture should follow a recurrence or meaningful workload change, rather than repeatedly sampling the same healthy state.

1. **Publish the coordinated consolidation releases.** Accepted-dev native/Pi/public validation and the changelog/source handoff are complete. Maintainers choose versions, create signed release commits/tags, promote main and verify release artifacts. Follow [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md). Pause new analytics until this breakpoint; this release does not claim complete CoreScope parity.
2. **Continue listed issue #12 in small screen groups.** The English/French foundation #62 is merged; RF / Signal (#63), Paths & Hashes (#64), Traffic (#65), Scopes (#66) and Clock Drift (#69) are ready for review. Prioritize #68 for #67. Shared Timestamp wording is next while reviewed; Talkers translation follows the fix. Preserve identifiers and measurement semantics. Other page, chart and dialog text remains; keep partial coverage explicit. Refresh all open issues/reviews before choosing the next group.
3. **After the consolidation release: Channel Activity analytics.** Inspect existing aggregates and add bounded channel traffic/trend views. Define messages versus receptions, unknown/encrypted-channel coverage and the behavior when keys are unavailable. Keep keys and message contents out of aggregate responses; avoid raw-message paging to build statistics.
4. **Observed ambiguity and topology.** Separate static prefix conflicts from observed unresolved/ambiguous paths. Add justified route-pattern, neighbour, hop and distance views with clear provenance and bounded work.
5. **Administration and backup slices.** Non-destructive archive validation is merged in #160. Resolve browser login/session and restore authorization before an import endpoint; keep deployment-file coverage and remote/scheduled backup separate. Test restoration against disposable databases. These follow-ups do not delay the current release.
6. **Production evidence and handoff.** Reconcile history, operational limits and the parity matrix below before preparing a release/cutover handoff.

## Listed work still open

| Issue | Remaining scope |
|---|---|
| [Server #116](https://github.com/MeshCore-Beacon/beacon-server/issues/116) | No recurrence in the September 20 retained log / ten-minute capture; still needs an attributable event with callback/pool timing |
| [Server #99](https://github.com/MeshCore-Beacon/beacon-server/issues/99) | Advert names and ACK/TRACE/PING references are accepted; define any remaining packet-type formats |
| [Server #60](https://github.com/MeshCore-Beacon/beacon-server/issues/60) | Remaining administration/worker/persistence behavior; account records do not establish login sessions |
| [Server #72](https://github.com/MeshCore-Beacon/beacon-server/issues/72) | Download #154 and archive validation #160 are accepted; import, browser access, deployment-file coverage and remote/scheduled backup remain |
| [Web #67](https://github.com/MeshCore-Beacon/beacon-web/issues/67) | Stale Talkers display states are fixed in independent #68; closes on merge into dev |
| [Web #12](https://github.com/MeshCore-Beacon/beacon-web/issues/12) | Foundation #62 is merged; Signal #63, Paths #64, Traffic #65, Scopes #66 and Clock Drift #69 are in review. Shared Timestamp wording is next; Talkers follows #68, with other screens/dialogs/formatting remaining |

The six completed analytics/icon/map issues are closed. Refresh the six currently open issues first at every continuation; accepted partial contributions are not grounds to close broader issues. Use closing references only when a PR completes the issue's accepted scope; use related references for partial work.

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
