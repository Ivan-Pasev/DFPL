# PRIMA §10 — Executable RP0 Campaign and Evidence-Based Promotion/Redesign

**Status:** Active execution campaign — 2026-09-04

## 10.0 Purpose
§10 records actual execution against the §9 RP0 adjudication gate. It separates three maturity layers: vector contract, deterministic persisted-state model, and real durable runtime/backend evidence.

## 10.1 Materialized F0–F12 pack
`prima/vectors/rp0-failure-candidate-0001.json` now materializes one candidate scenario for every stable failure point F0–F12, including the expected authority, budget, dedup, receipt, UnknownOutcome, checkpoint and lease invariants.

The vector pack is `DRAFT_UNVERIFIED` until exercised by the applicable runtime harness. Its existence alone is not R1/R2 evidence.

## 10.2 G1 deterministic persisted-state model
The private laboratory now contains `prima-runtime-rs`, a deliberately small Rust model of the durable state relevant to F0–F12. The model excludes ephemeral recovery state and represents message pending/ack, dedup, consumed authority, remaining budget, Decision/Authorization/intent/receipt persistence, UnknownOutcome, checkpoint generation, lease epoch and logical state version.

The first GitHub Actions execution on Ubuntu 24.04.4 with Rust/Cargo 1.98.0 passed 9 tests and executed all 13 failure points. Observed model behavior included:

- F0–F2: no durable commit is invented;
- F3: post-commit/pre-ack redelivery is deduplicable and consumed authority/budget persist;
- F6: AuthorizationArtifact does not imply execution;
- F7: execution intent is not execution proof;
- F8/F9: ambiguous external submit/response gaps recover as durable `UnknownOutcome`;
- F10: receipt persists before dependent state advancement;
- F11: the last valid checkpoint remains authoritative after failed/corrupt next write;
- F12: takeover advances the fencing epoch without resetting authority/budget/dedup state.

## 10.3 Model evidence is not runtime conformance
A passing deterministic model demonstrates that the intended state-transition invariants are executable and internally consistent for the model. It does NOT establish:

- a transactional durable mailbox implementation;
- filesystem/database crash durability;
- real acknowledgement atomicity;
- concurrent process lease fencing;
- external adapter correspondence;
- cross-backend reproduction;
- R1 or R2.

Therefore the §9 adjudication remains `HOLD_HARNESS_INCOMPLETE`, narrowed to the absence of a real durable reference backend campaign.

## 10.4 Backend A target
The first real Backend A SHOULD implement RP0 over a simple transactional durable store with explicit crash/reopen semantics. SQLite is a suitable laboratory candidate because one local transactional database can model mailbox, dedup, state, replay/authority, budgets, receipts, checkpoints and leases while retaining inspectable durability behavior. Backend choice does not become normative PRIMA semantics.

Backend A evidence MUST execute the public vectors through actual commit/rollback/reopen boundaries rather than directly assigning expected model states.

## 10.5 Backend B target
Backend B MUST reproduce the declared RP0 safety invariants under a distinct backend or materially independent persistence configuration. Equivalent canonical runtime artifacts/frontiers are required; identical physical storage bytes are not.

## 10.6 Promotion discipline
- Model PASS: useful G1 evidence only.
- Backend A single-environment PASS: still insufficient for R1/R2 `PASS_REPRODUCED`.
- Backend A repeated + Backend B reproduction over mandatory vectors: eligible for §9 adjudication.
- R3/R4 remain independent stronger campaigns.

## 10.7 Current adjudication
Current result:

`HOLD_HARNESS_INCOMPLETE`

Progress since §9: F0–F12 vectors are materialized and the deterministic persisted-state model executes successfully. Remaining blocker: real durable Backend A/B evidence and handoff/runtime artifact integration.

## 10.8 Next executable target
Implement actual transactional mailbox/state/replay/budget/receipt/checkpoint/lease stores, run F0–F12 with process-style reopen/recovery, then reproduce the mandatory subset on Backend B. Preserve all failure traces.

**NEXT:** §11 — Durable Backend A/B Evidence and R1/R2 Adjudication, only after real backend campaigns exist.