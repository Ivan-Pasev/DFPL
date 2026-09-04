# PRIMA §9 — RP0 Reference Runtime Adjudication, Cross-Backend Reproduction, and Promotion Decision

**Status:** Active evidence gate — 2026-09-04

## 9.0 Purpose
§9 defines how PRIMA-RP0-DURABLE-MAILBOX-v1 earns runtime conformance claims. It does not award R1/R2 from architecture or source-code inspection. Claims require persisted-state failure injection and reproduced evidence.

## 9.1 Reference campaign
The reference runtime candidate MUST implement the §6–§8 contract, including durable mailbox/dedup, per-agent sequential leased processing, local atomic acknowledgement transaction, durable replay/authority/budget/checkpoint state, execution-intent records, OutcomeReceipt/UnknownOutcome handling, F0–F12 injection and handoff artifacts.

## 9.2 Deterministic driver
A test driver MUST control message order, lease epochs, logical time inputs, mock-adapter outcomes, injected crash point and restart sequence. Recovery is evaluated from persisted state only; hidden process memory cannot be part of the oracle.

## 9.3 Backend A and Backend B
R1/R2 `PASS_REPRODUCED` requires the campaign to execute in at least two declared environments or durable-store backends with equivalent RP0 semantics. The evidence report identifies backend versions, transaction/isolation assumptions and filesystem/database durability assumptions.

Cross-backend reproduction is not required to produce identical physical storage bytes. It MUST produce equivalent canonical runtime artifacts, state frontiers, authority/replay/budget consumption and externally observable RP0 outcomes.

## 9.4 Failure-injection adjudication
Each F0–F12 point MUST have at least one materialized vector. For every injected crash the report records pre-crash durable state, injected point, restart durable state, resumed action, resulting artifacts and expected invariant outcome.

Failures remain in the campaign ledger after fixes.

## 9.5 R1 gate
R1-DURABLE-LOCAL requires reproduced evidence for stable MessageID/dedup, sequential processing, atomic local state/checkpoint/replay/budget update before ack, crash-safe redelivery, authority non-resurrection and durable receipt/state progression.

## 9.6 R2 gate
R2-FAILURE-RECOVERY additionally requires reproduced F0–F12 recovery behavior, lease takeover/fencing, durable UnknownOutcome, safe retry classification, checkpoint corruption handling and deterministic recovery decisions under the declared profile.

## 9.7 R3/R4 boundary
R3 and R4 are not implied by R1/R2. Cross-runtime handoff and stronger external-effect assurance require their own vector families and evidence. A local runtime PASS cannot be relabeled as distributed/external exactly-once behavior.

## 9.8 Handoff reproduction
The cross-runtime campaign MUST preserve AgentID/incarnation lineage, checkpoint frontier, dedup frontier, consumed replay/authorization state, budgets, receipt frontier, unresolved UnknownOutcome set and lease/fencing state. Tampered, stale or replayed handoffs MUST be rejected according to §7.

## 9.9 Promotion decisions
Adjudication result is one of:

- `HOLD_HARNESS_INCOMPLETE`
- `HOLD_VECTOR_INCOMPLETE`
- `HOLD_RUNTIME_FAILURE`
- `HOLD_BACKEND_DIVERGENCE`
- `HOLD_HANDOFF_DIVERGENCE`
- `PROMOTE_R1`
- `PROMOTE_R1_R2`
- later explicit R3/R4 decisions.

Promotion is scoped to the exact runtime profile, implementation commit, backend/environment assumptions and corpus version recorded in evidence.

## 9.10 Current adjudication
As of 2026-09-04, the public RP0 corpus/evidence contract exists but the reference harness has not produced reproducible F0–F12 evidence and no cross-backend campaign is recorded. Therefore no R1/R2 promotion is justified.

Current result: `HOLD_HARNESS_INCOMPLETE`.

## 9.11 Obligations
T-ADJ-RP0-01 Persisted-State Oracle; T-ADJ-RP0-02 Failure Preservation; T-ADJ-RP0-03 Backend Assumption Disclosure; T-ADJ-RP0-04 R1 Gate Soundness; T-ADJ-RP0-05 R2 Gate Soundness; T-ADJ-RP0-06 UnknownOutcome Preservation; T-ADJ-RP0-07 Authority Non-Resurrection; T-ADJ-RP0-08 Handoff Frontier Preservation; T-ADJ-RP0-09 Scoped Promotion; T-ADJ-RP0-10 No Exactly-Once Overclaim.

## NEXT
Implement and execute the RP0 harness, materialize F0–F12 vectors, reproduce on Backend B, and promote only the classes supported by the resulting evidence.