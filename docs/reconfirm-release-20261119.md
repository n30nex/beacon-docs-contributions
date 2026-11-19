# Beacon route maintenance release-host check

19 November 2026 · Server issue #224 · Canadaverse maintainer handoff

**The October failure did not recur in the sampled release window.** The route cursor advanced, and the independently scheduled hourly neighbour query returned to idle in 206 ms on the release host. The release and dev hosts were inspected read-only. Three focused draft fixes were deployed together on Canadaverse. [Release-host observations on #224](https://github.com/MeshCore-Beacon/beacon-server/issues/224#issuecomment-7007379527)

## Scheduled maintenance on the release and dev hosts

| Host | Running server source | Common log window, UTC | Logged statement timeouts / skipped-slice warnings | Observed neighbour query, UTC |
| --- | --- | --- | --- | --- |
| live.meshcore.ca | [265a835e3693](https://github.com/MeshCore-Beacon/beacon-server/commit/265a835e36931a2c39b9b08e7a78837b9cf0e343) | 03:53–11:07 | 0 / 0 | 10:53:43 · 206 ms |
| dev.meshcore.ca | [c255001ff44f](https://github.com/MeshCore-Beacon/beacon-server/commit/c255001ff44f6ff1764842f69d0ec806660ade5c) | 10:05–11:07 | 0 / 0 | 11:05:34 · 190 ms |

The release image matched upstream main and v2.2.0. Dev served API 2.3.0 from the image revision shown above. The older issue originated on dev1. The two measurements here are from the running release and dev instances.

Each observation matched the hostname, running server image, application database and PostgreSQL session. The release cursor changed between the 10:48 and 10:53 saved checkpoints, and advanced again. The hourly grace watermark was persisted immediately before the neighbour query. The durations in the table measure PostgreSQL query start to idle. Neither host logged an error within ten seconds of its observed neighbour query or a task failure for that pass.

We also sampled the following hour on both hosts.

- live.meshcore.ca returned to idle again at 11:53:43 UTC after 175 ms. The subsequent PostgreSQL read found zero logged statement timeouts through 12:05 UTC.
- dev.meshcore.ca was sampled again at 12:05 UTC. This second sample did not capture the neighbour statement.

PostgreSQL recorded errors to the collected stderr stream at both sites. All database log records retained since the current application processes started fit within the read cap. The counts apply to the windows shown. Both sites used info-level application logs. The statement statistics extension was installed without preloading, so per-query lifetime totals were unavailable. No maintenance run, SQL plan, configuration change or restart was requested on either host.

## Changes ready for upstream review

| Draft | What changed | Evidence |
| --- | --- | --- |
| [Server #349](https://github.com/MeshCore-Beacon/beacon-server/pull/349) | Count routes actually present in a timed-out final slice when deciding whether to wrap. | A PostgreSQL fixture with two routes and a locked first candidate reported ten skipped on dev. The fix recorded two timeouts and two skips, then deleted both eligible routes after release of the lock. The generated query passed empty, short, full and cross-region boundary checks. |
| [Server #350](https://github.com/MeshCore-Beacon/beacon-server/pull/350) | Check each distinct neighbour and IATA once, using a bounded lookup for a unique four-byte regional identity. | A restored sample and a separate nonempty deletion fixture matched the old query in both directions. Three-byte prefix matches and reuse in a different IATA remain valid. |
| [Server #351](https://github.com/MeshCore-Beacon/beacon-server/pull/351) | Report timed-out statements and cycle wraps at info level. Emit hourly completion after successful neighbour revalidation. | Tests cover ordinary debug-level slices, recovered timeouts, partial errors and a failing final neighbour step. The deployed preview logged its naturally scheduled completion at 13:05:23 UTC. |
| [Docs #75](https://github.com/MeshCore-Beacon/beacon-docs/pull/75) | Explain the completion field, statement timeout count, deferred row count and checkpoint order. | Publish with server #349 and #351. |

## Query performance

The measurements came from a private PostgreSQL 16 copy with 31,412 neighbour edges and 16,746 regional short IDs. Both queries ran eight times after warm-up in alternating order. Each measured DELETE was rolled back.

| Median per pass | Previous query | New query |
| --- | ---: | ---: |
| Execution time | 124.1 ms | 28.7 ms |
| Shared buffer hits plus reads | 157,654 | 35,151 |
| Temporary blocks written | 0 | 0 |

The first draft reduced the full-table median to 21.4 ms but regressed at intermediate cardinality. At 1,024 edges PostgreSQL repeatedly scanned a materialized list of identities, taking 824 ms against about 9 ms on upstream. That build was withdrawn from the preview and the previous backend was verified before the revised cutover. The revised statement checks each distinct regional neighbour with an indexed lateral lookup.

The sensitivity check sampled the same catalogue into temporary edge tables. Each row is the median of five warm, alternating runs per query. The empty-table case has a small fixed overhead.

| Edges | PostgreSQL work_mem | Upstream | Revised |
| ---: | --- | ---: | ---: |
| 0 | 4MB | 0.05 ms | 0.12 ms |
| 1 | 4MB | 0.26 ms | 0.16 ms |
| 32 | 4MB | 0.56 ms | 0.43 ms |
| 256 | 4MB | 6.43 ms | 1.27 ms |
| 1,024 | 4MB | 9.26 ms | 2.43 ms |
| 4,096 | 4MB | 20.03 ms | 4.46 ms |
| 31,412 | 4MB | 115.85 ms | 27.23 ms |
| 1,024 | 64kB | 5.24 ms | 2.45 ms |
| 31,412 | 64kB | 134.59 ms | 42.56 ms |

The restored edges were clean, so both queries selected zero deletions. In a separate transaction, 700 added edges covered missing identities, wrong regions, true full-prefix collisions and shorter shared prefixes. Both queries selected the same 400 deletions, the candidate deleted exactly 400, and all 300 expected survivors remained. The transaction rolled back. Buffer counts include repeated touches. Production latency and cold-cache performance were not benchmarked.

We also tested five stale-edge scenarios. Both versions removed the same number of edges on every run. With 15,775 of 31,412 edges stale and 4 MiB of work memory, median time fell from 65.6 to 34.2 ms. With the same stale edges and only 64 KiB, median time increased from 86.5 to 99.5 ms. When every regional short ID was assigned the same full prefix in the stress fixture, both versions removed 31,412 edges, taking 10.61 seconds and 279 ms respectively. These are four-run medians on temporary tables.

## Reproducing the checks

Point `BEACON_TEST_POSTGRES_DSN` at a disposable PostgreSQL 16 database with Beacon's schema before running these checks.

~~~sh
go test ./db -count=1 -run '^TestReconfirm.*Postgres$' -v
go test -race ./internal/background -count=1
~~~

For a plan comparison, use the named `ReconfirmNeighbors` statement from each source revision against a restored database. `EXPLAIN (ANALYZE, BUFFERS)` executes the deletion. Run each sample inside its own transaction and roll it back. Compare both complete key sets and test intermediate edge counts as well as the full table.

## Preview acceptance

The deployed ARM64 binary and public source archive matched the Actions build for [f3ecec5e602a](https://github.com/n30nex/beacon-server-contributions/commit/f3ecec5e602a270a3dcc65d1dbaca1a856c9553a). All three upstream drafts and the combined fork passed CI. Tests included Go build, vet, the full server suite, background race checks, generated SQL consistency, PostgreSQL regressions, query-plan checks and backup recovery. [Combined CI](https://github.com/n30nex/beacon-server-contributions/actions/runs/44517834388) · [Binary and source artifact](https://github.com/n30nex/beacon-server-contributions/actions/runs/44517834432)

After startup the preview advanced its route checkpoint on the normal five-minute cadence. The hourly run persisted its grace checkpoint and logged info-level neighbour completion at 13:05:23 UTC. The same server process remained up throughout qualification. The operator's one-hour interval was preserved. A read-only PostgreSQL sample measured 347.5 ms from the start of this neighbour statement to idle on the preview.

Frontend and mobile revisions stayed at `c59ee53a8045` and `c11b1b277f91`. The web suite passed 2,330 tests. Flutter passed 1,086 tests with 16 optional screenshots skipped. Public readback verified 82 web assets, 36 English/French desktop and touch page visits, two real map sessions, four ticketed WebSocket profiles and both MQTT brokers. Beacon API errors during the page sweep were zero. The browser recorded 1 distinct external font tile fallback(s). Touch checks used browser emulation.

The fresh web test count comes from the project's Linux CI environment. On this Windows workstation, the separate local run could not run the POSIX Docker entrypoint tests with its default shell path. Adding Git's shell still exposed path differences in the inline-HTML cases. The served bundle was verified independently in Chromium. [Web CI rerun](https://github.com/n30nex/beacon-web-contributions/actions/runs/44505141229/attempts/2)

## Recovery

The only deployed component was the Canadaverse backend. The ledger stayed at 88 migration entries. The previous binary and container are retained at checkpoint `reconfirm-final-server-20261119T120505Z`. From the existing preview directory on the Pi, run `sudo python3 evidence/reconfirm-release-20261119/backend-final/deploy-server.py rollback` to restore server `6c3af05dbc69`. This operation preserves current web and native artifacts and accumulated application data. The intermediate preview checkpoint was actually rolled back to this prior binary, and both brokers reconnected. A subsequent read-only check confirmed that the parked container, both executable hashes, the restart script, nonbinary mounts and protected configuration match the saved checkpoint.

The release-host check requested on #224 is complete for the stated window. The issue remains open for its maintainer’s disposition. The three code drafts remain independently reviewable.

## Remaining priority work

At the queue check, each of the six other open high-priority bugs in the server, web and Flutter repositories had a mergeable draft targeting `dev`. The existing server reviews cover subscription ordering, concurrent cache misses, backfill pressure and suspect traces. [Server #330](https://github.com/MeshCore-Beacon/beacon-server/pull/330) · [#298](https://github.com/MeshCore-Beacon/beacon-server/pull/298) · [#306](https://github.com/MeshCore-Beacon/beacon-server/pull/306) · [#307](https://github.com/MeshCore-Beacon/beacon-server/pull/307)

The two client reviews cover restoring and exchanging valid large Atlas collections. [Web #233](https://github.com/MeshCore-Beacon/beacon-web/pull/233) · [Flutter #48](https://github.com/MeshCore-Beacon/beacon-flutter-app/pull/48)
