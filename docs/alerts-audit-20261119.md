# Beacon alert delivery and profile performance

19 November 2026 · Canadaverse preview · Maintainer handoff

Four independent draft pull requests target upstream `dev`. Canadaverse runs the combined server and web fixes. The Flutter contribution fork has a tested Android build. The preview keeps accounts, alert delivery and polling disabled.

## Fixes for review

| Change | Reproduction and result | Draft |
| --- | --- | --- |
| Count push retry delays from receipt | A relay reply 90 seconds into a pass asking for another 60 seconds previously produced an expired deadline. The corrected deadline is 60 seconds after the reply. Six cases cover batch and item errors, including default waits. | [Server #344](https://github.com/MeshCore-Beacon/beacon-server/pull/344) |
| Skip work when nobody has a registered device | With 300 notices for users without devices, the sender now performs zero delivery-history reads per batch, down from one. Allocations fell from 2,126 to 26, and allocated bytes from 212,475 to 51,617 per batch. These are medians across five in-process samples per version. Mixed-device and mail settlement are exercised separately. | [Server #345](https://github.com/MeshCore-Beacon/beacon-server/pull/345) |
| Open alert editors on demand | With 100 radios and eight rules per radio, the profile mounted 800 editors on load. It now mounts zero, then eight after opening one radio and 16 after opening a second. An edited threshold survived collapse and keyboard reopening. Both English desktop and French touch profiles fetched the alert list once. | [Web #249](https://github.com/MeshCore-Beacon/beacon-web/pull/249) |
| Serialize native channel changes | Two rapid inputs previously sent two preference writes, each returning both channel values. One change can now be pending. Switching push on keeps the controls busy until device registration finishes. Tests delay both the preference response and the device response. | [Flutter #52](https://github.com/MeshCore-Beacon/beacon-flutter-app/pull/52) |

The backend and mobile source tests use controlled relay and registration responses. The profile test uses isolated browser fixtures with no account writes. The allocation measurements describe one workload with a fake store. They do not measure network latency or production CPU.

## Candidate and tests

| Component | Upstream dev included | Qualified preview source | Evidence |
| --- | --- | --- | --- |
| Server | [c89c1e924c00](https://github.com/MeshCore-Beacon/beacon-server/commit/c89c1e924c0007c12c18c5b13667bf33e2d0e718) | [6c3af05dbc69](https://github.com/n30nex/beacon-server-contributions/commit/6c3af05dbc690afc9fd03c2d219e98ed1286ad0d) | [CI](https://github.com/n30nex/beacon-server-contributions/actions/runs/44503882586) · [Build](https://github.com/n30nex/beacon-server-contributions/actions/runs/44503882335) |
| Web | [e5269459dd16](https://github.com/MeshCore-Beacon/beacon-web/commit/e5269459dd16d9494e21aa528a8e14a9cb198484) | [c59ee53a8045](https://github.com/n30nex/beacon-web-contributions/commit/c59ee53a8045ac3969e2599fd69c66d72f6017a2) | [CI](https://github.com/n30nex/beacon-web-contributions/actions/runs/44505141229) · [Build](https://github.com/n30nex/beacon-web-contributions/actions/runs/44505127727) |
| Flutter | [f5ee4fc459fd](https://github.com/MeshCore-Beacon/beacon-flutter-app/commit/f5ee4fc459fdb9765dd7947982c657bf30103adc) | [c11b1b277f91](https://github.com/n30nex/beacon-flutter-app/commit/c11b1b277f91475b457b205d1201fea2aa36f45f) | [CI](https://github.com/n30nex/beacon-flutter-app/actions/runs/44502455079) · [Build](https://github.com/n30nex/beacon-flutter-app/actions/runs/44502458181) |

The final web build includes both upstream fixes for mailed links during startup and region selection. Its Linux suite passed **2,330 tests across 219 files**. All **82 publicly served web files** matched the build after accounting for the documented Cloudflare HTML injection. Web and server source archives matched their commit trees. The running ARM64 binary matched its build digest.

The composed server passed the full Go suite, PostgreSQL 16 integration, plan and backup/recovery checks. The alert sender passed a separate race run. Browser acceptance covered 36 page visits across English and French, desktop and phone-sized touch emulation. Two real-feed map sessions checked animation start, stop, navigation and reduced motion. Four ticketed WebSocket combinations received live events. Both MQTT brokers were connected. The 100-radio fixture ran on the baseline, the staged bundle and the public build.

The composed Flutter suite passed **1,086 tests**, with 16 optional screenshots skipped. One Windows parallel run left a packet-filter test unfinished. Its isolated rerun, a full single-worker Windows run and Linux CI passed on the same source. The Android debug APK is version 2.3.0, build 2, with verified SHA-256 `f9c0cb4a44aefd7d4aafc7bf3bcdc135961edec2dd609064735b1aecaf3b99bd`. Its debug certificate differs from the previous build. An in-place upgrade over that build requires matching signing keys. Physical device delivery, Apple Push Notification service and Firebase Cloud Messaging delivery remain unverified.

One snapshot caught a periodic map read in flight. The repeated sweep tracked the outstanding request through completion. The French desktop map also requested a glyph tile missing from OpenFreeMap. A direct read confirmed HTTP 404 for that range, and MapLibre reported rendering U+10990 locally. The existing content security policy blocked optional Cloudflare analytics. All Beacon API reads in the page sweep completed without an HTTP error. [Provider glyph tile](https://tiles.openfreemap.org/fonts/Noto%20Sans%20Regular/67840-68095.pbf)

## Relay and preview settings

The public relay responded with HTTP 200 and `ok` at 2026-11-19 09:34 UTC. The relay repository passed its local tests, build and vet. Its health endpoint checks whether the service answers. Issuing a push identity, enrolling a phone and delivering a real notification are separate operator checks. A Beacon server that offers push advertises it through `/api/v1/info`. Canadaverse advertises both alert channels off, retains its existing Atlas and map telemetry display capability, and reports minimum web and app versions of 2.3.0. [Relay health](https://push.meshcorebeacon.ca/healthz) · [Operator setup](https://github.com/MeshCore-Beacon/beacon-docs/blob/dev/docs/alerts.md#push)

## Database upgrade and recovery

Upstream migrations 084 and 085 add channel preferences and device payload keys, and split retry state by channel. Migration 084 clears pre-existing device registrations. A full private preview backup was restored on isolated PostgreSQL 16 before deployment. Counts for all 80 application tables survived the upgrade. The inverse restored the original alert columns, constraints, indexes and ledger. A second upgrade succeeded.

Immediately before changing the preview, the users, device registrations and alert outbox tables were empty. The upgrade verified that again under table locks, applied both migrations in one transaction, and checked the new database fingerprint. The preview ledger advanced from 86 to 88 entries including three retained historical entries. The other containers, private settings and radio services passed their before/after checks. This empty-table recovery procedure is specific to Canadaverse. Sites with registered devices need their own upgrade and re-enrollment plan.

From the existing Canadaverse preview directory, run the following in order to restore the November 17 web and server pair. The cutover scripts verify their target, checkpoint and schema. If account, device or queued delivery rows have since appeared, the server rollback stops for operator review.

1. Restore the frontend with `sudo python3 evidence/alerts-audit-20261119/web-runtime/deploy-web.py rollback`. Checkpoint `alerts-web-20261119T103707Z`.
2. Restore the backend with `sudo python3 evidence/alerts-audit-20261119/backend/deploy-server.py rollback`. Checkpoint `alerts-server-20261119T103630Z`.

The schema inverse was exercised on the restored copy. The running services were verified after the forward cutover. A live rollback was not rehearsed.

## Open release check

The persisted Canadaverse route-reconfirmation cycle counter advanced from 48 on November 17 to 51 on November 19 on the preceding server build. The release-host check still needs a measured count of skipped or timed-out slices and evidence that neighbour revalidation completes under its own workload. [Server issue #224](https://github.com/MeshCore-Beacon/beacon-server/issues/224)
