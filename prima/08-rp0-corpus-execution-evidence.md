# PRIMA §8 — RP0 Machine-Readable Event/Handoff Corpus and Reference Runtime Execution Evidence

**Status:** Freeze candidate — 2026-09-04

## Purpose
§8 converts PRIMA §§5–7 and `PRIMA-RP0-DURABLE-MAILBOX-v1` into executable evidence obligations. It defines the machine-readable runtime vector corpus, failure-injection execution report, event/handoff artifact vectors and the promotion gate for RP0 R1/R2.

## RP0 corpus manifest
`RP0CorpusManifest` binds `{runtime_profile_id, corpus_version, schema_refs[], vector_refs[], failure_points[], required_classes[], backend_matrix[], known_gaps[], corpus_digest}`.

Each vector binds initial durable stores, input messages/events, optional failure point, expected durable post-state, expected artifact identities/relationships, expected receipts/UnknownOutcome/lease state and status.

## Required vector families
At minimum:

1. stable MessageID across redelivery;
2. duplicate logical message dedup;
3. conflicting payload under reused MessageID rejection;
4. enqueue-order persistence;
5. F0–F3 delivery/local-transaction/ack crashes;
6. F4–F7 verification/authorization/execution-intent crashes;
7. F8–F10 ambiguous external submit/receipt/state-advance crashes;
8. F11 checkpoint write failure/corruption;
9. F12 lease takeover/stale fencing;
10. one-shot authorization non-resurrection;
11. budget persistence/non-amplification;
12. UnknownOutcome durability and reconciliation;
13. idempotent retry using stable key;
14. non-idempotent ambiguous retry rejection;
15. receipt-before-dependent-progress;
16. dead-letter/backpressure behavior;
17. EventID causal-DAG reproduction;
18. CheckpointID frontier sensitivity;
19. Handoff prepare/accept/source-retire state machine;
20. cross-runtime authority/budget/receipt/UnknownOutcome/dedup preservation;
21. incompatible target rejection;
22. handoff tamper/replay rejection;
23. concurrent incomparable trace events.

## Deterministic driver
The reference testkit exposes a deterministic logical driver. It controls delivery order, failure point, lease acquisition/takeover, mock-adapter responses and reconciliation observations. Wall-clock timing is not required to reproduce the safety vectors.

## Failure injection
F0–F12 are stable corpus identifiers. A run records whether the injected failure occurred before/after each declared durable boundary and which stores committed. The harness must restart/recover from persisted state rather than continuing from in-memory state after a simulated crash.

## Mock effect adapter
The first adapter must deterministically support: success; rejection/failure; timeout; response loss; external effect with lost response; duplicate submit; stable idempotency-key replay; non-idempotent ambiguity; delayed reconciliation; observed-state divergence. Mock results are test evidence for runtime semantics only, not evidence of a real external integration.

## Runtime artifact identities
Vectors must exercise the §7 candidate identities: MessageID, EventID, CheckpointID and HandoffID. Expected IDs remain `DRAFT_UNVERIFIED` until the owning canonical registries/encodings are fixed and reproduced.

## Cross-runtime handoff harness
The harness runs at least two distinct runtime instances/configurations sharing only the declared portable artifacts/store interface. It exercises `PrepareHandoff -> source fence/quiesce -> checkpoint/frontier commit -> AcceptHandoff -> target lease/incarnation -> recovery validation -> target activation`.

The target must not activate privileged work if required authority/replay/budget/receipt/UnknownOutcome or fencing state cannot be preserved.

## R1 promotion gate
RP0 R1-DURABLE-LOCAL requires reproducible execution of the mandatory local mailbox/dedup/state/checkpoint/replay/budget vectors across restart with an evidence report containing implementation commit, toolchain, backend version, corpus digest, commands, pass/fail/skip details and artifact digests.

## R2 promotion gate
RP0 R2-FAILURE-RECOVERY additionally requires reproducible F0–F12 coverage, durable UnknownOutcome/reconciliation vectors, receipt-before-progress, idempotency/non-idempotency cases and no authority/budget resurrection.

## R3/R4 boundary
R3 requires an explicitly declared distributed lease/fencing backend and concurrent stale-holder/takeover evidence. R4 is adapter-specific and cannot be inferred from mock-adapter success.

## Evidence statuses
`NOT_RUN | FAIL | PASS_SINGLE_ENV | PASS_REPRODUCED | PASS_DIFFERENTIAL | SKIPPED_WITH_REASON`.

Only `PASS_REPRODUCED` or stronger may support an R1/R2 conformance claim.

## Evidence package
`RP0EvidenceReport` binds runtime profile/class, implementation commit, corpus digest, environment/toolchain/backend, executed vectors, failure-injection coverage, artifact IDs/digests, command transcript/reproduction entrypoint, known exclusions and overall adjudication.

## Property targets
T-EVID-01 Crash-Recovery Reproducibility; T-EVID-02 Failure-Point Coverage; T-EVID-03 Persisted-State-Only Recovery; T-EVID-04 Message Dedup Safety; T-EVID-05 Authority/Budget Non-Resurrection; T-EVID-06 Receipt Progression; T-EVID-07 UnknownOutcome Reconciliation; T-EVID-08 Handoff Frontier Preservation; T-EVID-09 Stale-Source Fencing where claimed; T-EVID-10 Evidence-Report Binding.

## Freeze consequence
RP0 now has an executable evidence contract. The next milestone is a real harness run and reproducible R1/R2 evidence, not a prose conformance assertion.

## NEXT
§9 — RP0 Reference Runtime Adjudication, Cross-Backend Reproduction, and Promotion Decision.