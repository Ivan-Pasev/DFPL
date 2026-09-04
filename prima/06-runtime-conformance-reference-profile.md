# PRIMA §6 — Runtime Conformance and Reference Profile

**Status:** architectural normative draft / freeze candidate

## 6.0 Purpose

PRIMA §6 turns the abstract runtime guarantees of §5 into one minimal reference profile that can be implemented, failure-injected, replayed, and independently tested.

The reference profile is intentionally conservative. It prefers explicit durable state, stable identifiers, single-agent sequential processing, at-least-once delivery with deduplication, and receipt-driven progression over stronger guarantees that are difficult to establish across external effects.

The goal is not to prescribe one production runtime. It is to define a falsifiable baseline against which implementations can claim a specific conformance class.

## 6.1 Reference profile identifier

The first profile is named:

```text
PRIMA-RP0-DURABLE-MAILBOX-v1
```

A concrete implementation MUST bind the exact profile version it claims.

The profile is not a DFPL Kernel version and does not alter DFPL semantic meaning.

## 6.2 RP0 design envelope

RP0 provides:

- one logical mailbox per AgentID;
- at-least-once message delivery;
- stable MessageID across redelivery;
- persistent deduplication state;
- sequential processing per logical AgentID;
- explicit AgentIncarnation identity;
- durable AgentState;
- durable checkpoints;
- durable OutcomeReceipt references;
- durable replay/authorization-consumption state;
- explicit UnknownOutcome reconciliation state;
- lease/epoch ownership for exclusive active incarnation;
- failure injection at specified boundaries;
- no global cross-agent ordering guarantee;
- no exactly-once external-effect claim.

## 6.3 Minimum storage interfaces

A conforming implementation exposes logical stores equivalent to:

```text
MailboxStore
AgentStateStore
CheckpointStore
ReceiptStore
ReplayStateStore
LeaseStore
DeadLetterStore
```

These MAY share one database/transaction engine, but their logical semantics MUST remain distinguishable.

## 6.4 Canonical durable records

RP0 durable records include at least:

```text
MailboxRecord {
  message_id
  target_agent_id
  envelope
  enqueue_seq
  delivery_count
  acknowledged
}

AgentRuntimeRecord {
  agent_id
  state_version
  agent_state
  dedup_state
  pending_plan_refs[]
  pending_reconciliation_refs[]
  receipt_frontier
  budget_state
}

LeaseRecord {
  agent_id
  holder_incarnation_id
  lease_epoch
  expiry_or_validity_context
}
```

Implementations may use richer schemas but MUST preserve the same observable guarantees.

## 6.5 Transaction boundary

RP0 requires an atomic durable transaction for the local processing boundary:

```text
consume/dedup message
+ update AgentState
+ update replay/authorization-consumption state
+ persist produced internal events/messages
+ record checkpoint frontier
```

when all involved records are hosted in the RP0 durable store.

External effects are **not** included in this atomic transaction unless a concrete adapter proves a stronger transactional relationship.

## 6.6 Message enqueue semantics

Enqueue creates or identifies a durable mailbox entry by `message_id`.

If the same logical message is redelivered with the same MessageID and byte-equivalent canonical envelope, the mailbox may coalesce/deduplicate according to RP0 rules.

If the same MessageID arrives with conflicting content, the runtime MUST reject/quarantine it as an integrity conflict rather than choose one silently.

## 6.7 Delivery semantics

RP0 delivery is `AtLeastOnce` until acknowledgement.

A crash may cause the same unacknowledged message to be delivered again.

The runtime MUST therefore persist processed/dedup state before acknowledging a message whose reprocessing could duplicate durable agent consequences.

## 6.8 Acknowledgement point

RP0 acknowledges a message only after the local durable processing transaction has committed.

If processing produced a Plan that requires an external effect, message acknowledgement does not mean the external effect succeeded.

The Plan/authorization/effect/receipt lifecycle continues through explicit durable state.

## 6.9 Per-agent ordering

RP0 provides one total mailbox sequence per logical AgentID based on durable `enqueue_seq`.

The runtime processes one message/event at a time for an exclusively leased AgentID.

No ordering between different AgentIDs is guaranteed.

External event arrival time is not semantic unless represented explicitly in the message/evidence.

## 6.10 Scheduler model

A conforming RP0 scheduler MAY choose any runnable AgentID order.

For one leased AgentID, it MUST not process two mailbox items concurrently.

No liveness proof may assume fairness unless the implementation additionally claims and tests a fairness profile.

## 6.11 Incarnation and lease acquisition

Before processing an agent mailbox, an incarnation obtains the current lease:

```text
AcquireLease(agent_id, incarnation_id)
  -> lease_epoch | failure
```

Lease acquisition/increment MUST be atomic in the LeaseStore.

Every durable agent-processing transaction records the active `lease_epoch`.

## 6.12 Fencing

Where adapters support fencing, outbound effect attempts carry the active lease epoch or an equivalent monotone fence token.

A stale incarnation MUST be unable to commit fenced local runtime state after a newer lease epoch is established.

For external systems that cannot enforce fencing, the adapter MUST declare that limitation and RP0 conformance is limited accordingly.

## 6.13 Checkpoint rule

RP0 creates a checkpoint after every committed logical processing step or at a profile-declared coarser cadence that still permits deterministic recovery.

A checkpoint binds at least:

```text
AgentID
state version
mailbox acknowledged frontier
dedup state
replay/authorization-consumption state
budget state
receipt frontier
pending UnknownOutcome set
runtime profile ID
lease epoch
```

Checkpoint identity uses the canonical profile-defined encoding/CheckpointID construction.

## 6.14 Recovery algorithm

After crash/restart:

1. allocate a new IncarnationID;
2. acquire a new lease epoch;
3. load the latest valid checkpoint/AgentRuntimeRecord;
4. reconstruct dedup and acknowledgement frontier;
5. load pending Plans, authorizations, receipts and UnknownOutcome entries;
6. reconcile external uncertainty before replaying non-idempotent effects;
7. resume mailbox processing from the first unacknowledged eligible item.

Recovery MUST NOT infer success merely from a local intent record.

## 6.15 External-effect boundary

An RP0 operation follows:

```text
Durable Plan
 -> verified DecisionCertificate
 -> AuthorizationArtifact
 -> durable execution-intent marker
 -> EffectGateway attempt
 -> OutcomeReceipt or UnknownOutcome
 -> durable reconciliation/result update
```

A crash between external submission and receipt persistence is an explicit failure-injection point.

## 6.16 Execution intent marker

Before invoking a non-pure external effect, RP0 durably records an execution-intent object that binds at least:

```text
PlanID
OperationID
AuthorizationID
attempt_id
idempotency_key_or_none
lease_epoch
```

This marker does not prove execution. It exists so recovery can identify ambiguous attempts.

## 6.17 Idempotency keys

Where an adapter supports idempotency keys, RP0 derives or binds a stable key to the exact logical operation attempt.

Redelivery/recovery MUST reuse the same idempotency key for reconciliation/retry of that exact attempt rather than silently create a semantically new attempt.

If the target does not support idempotency, the adapter MUST classify duplicate-submit risk explicitly.

## 6.18 UnknownOutcome rule

If the runtime cannot determine whether an external effect occurred, it records:

```text
UnknownOutcome {
  plan_id
  operation_id
  attempt_id
  target_profile
  evidence_refs[]
  reconciliation_status
}
```

The message/agent may progress only according to explicit policy for unresolved outcomes.

RP0 MUST NOT automatically resubmit a non-idempotent effect merely because the process restarted.

## 6.19 Receipt persistence

OutcomeReceipts are persisted before agent state is advanced to a state that depends on their outcome.

The durable agent state stores receipt references/frontiers, not unsupported prose such as `success=true` without the corresponding receipt when the profile's claim relies on it.

## 6.20 Replay/authorization consumption

One-shot or bounded-use authority consumption is durable and part of the local atomic processing transaction where possible.

Restart, message redelivery, checkpoint restore, or lease transfer MUST NOT restore consumed authority.

## 6.21 Budget persistence

Safety/resource budgets are durable.

RP0 requires monotone consumption for each budget dimension unless a fresh explicit replenishment artifact/policy authorizes an increase.

A child agent, restart, or migration cannot obtain a larger remaining budget by cloning prior state.

## 6.22 Dead-letter rule

A message may enter DeadLetter only after an explicit profile-defined failure threshold or terminal classification.

Dead-lettering records:

```text
message_id
agent_id
failure_class
attempt_count
last_failure_ref
created_context
```

DeadLetter is observable failure/quarantine, not successful processing.

## 6.23 Backpressure

RP0 requires a finite mailbox capacity or explicit storage-quota policy.

When the limit is reached, the implementation MUST use one declared behavior:

```text
RejectProducer
ThrottleProducer
QuarantineOverflow
```

Silent dropping is not RP0-conformant.

## 6.24 Authentication boundary

RP0 does not mandate one transport-auth mechanism. A concrete implementation MUST declare one of its supported authentication profiles and must construct `sender_principal` only from authenticated runtime context.

Message authentication does not bypass PRIMA capability/authorization checks.

## 6.25 Time and timers

Timers generate explicit mailbox events.

RP0 may use local monotonic/wall clock for scheduling mechanism, but DFPL decisions that depend on time require explicit evidence/state according to the applicable Law/profile.

A timer firing is not itself a trusted time attestation.

## 6.26 Runtime conformance classes

Candidate PRIMA runtime conformance classes:

```text
R0-STRUCTURAL
R1-DURABLE-LOCAL
R2-FAILURE-RECOVERY
R3-DISTRIBUTED-LEASED
R4-EFFECT-ADAPTER-CONFORMANCE
```

### R0 — Structural

Implementation supports required object schemas/state machine interfaces but no durability/recovery claim.

### R1 — Durable Local

Passes durable mailbox, dedup, state, checkpoint, replay and budget persistence vectors under single-node restart tests.

### R2 — Failure Recovery

Passes deterministic failure-injection/recovery vectors including ambiguous external effects and UnknownOutcome persistence.

### R3 — Distributed Leased

Passes concurrent lease contenders, stale-incarnation rejection/fencing, takeover and split-brain detection vectors over the declared storage/adapter domain.

### R4 — Effect Adapter Conformance

Each claimed external adapter passes its own idempotency, attempt identity, receipt, reconciliation and observed-state correspondence suite.

Higher class claims include the lower classes they explicitly depend upon; an implementation MUST state its exact supported profile/adapters.

## 6.27 Required failure injection points

A reference implementation test harness MUST be able to stop/crash at least at:

```text
F0 before mailbox delivery
F1 after delivery before local transaction
F2 during local transaction before commit
F3 after local commit before acknowledgement
F4 after acknowledgement before Plan verification
F5 after DecisionCertificate before authorization
F6 after AuthorizationArtifact before execution-intent persistence
F7 after execution-intent persistence before external submit
F8 after external submit before response
F9 after response before OutcomeReceipt persistence
F10 after OutcomeReceipt persistence before AgentState advancement
F11 during checkpoint write
F12 during lease takeover
```

Each vector defines the allowed recovered state explicitly.

## 6.28 Core conformance scenarios

Mandatory RP0 scenarios include:

1. duplicate delivery of identical MessageID;
2. conflicting payload under reused MessageID;
3. crash before acknowledgement;
4. crash after local commit before acknowledgement;
5. one-shot authorization consumed before restart;
6. budget consumption before restart;
7. crash after external submit before receipt persistence;
8. idempotent retry with same key;
9. non-idempotent UnknownOutcome requiring reconciliation;
10. stale lease holder attempts to commit;
11. lease takeover after failure;
12. corrupted/missing checkpoint;
13. dead-letter transition;
14. mailbox overflow/backpressure;
15. receipt frontier reconstruction;
16. pending reconciliation survives restart.

## 6.29 Golden runtime vectors

Machine-readable runtime vectors SHOULD contain:

```text
vector_id
runtime_profile_id
initial_store_state
input_events[]
failure_injection_point?
expected_durable_state
expected_mailbox_state
expected_receipt_state
expected_replay_state
expected_budget_state
expected_unknown_outcomes[]
expected_lease_state
```

A vector is not considered passed from prose inspection; it must be executed against the implementation under test.

## 6.30 Reference implementation architecture

The preferred first implementation is intentionally small:

```text
prima-runtime-rs/
  store/
    mailbox
    agent_state
    checkpoint
    receipt
    replay
    lease
  runtime/
    scheduler
    dispatcher
    recovery
    supervision
  gateway/
    effect_adapter_trait
    mock_adapter
  testkit/
    failure_injector
    deterministic_driver
    golden_vectors
```

A single embedded transactional datastore MAY implement the initial durable-store backend, followed later by distributed profiles.

## 6.31 Mock effect adapter

The first conformance target SHOULD use a deterministic mock adapter able to simulate:

- success;
- explicit failure;
- delayed response;
- duplicate submit;
- idempotent replay;
- ambiguous submit/UnknownOutcome;
- observed post-state divergence.

This allows RP0 failure semantics to be tested before binding conformance claims to real external services.

## 6.32 Deterministic test driver

A test driver SHOULD control:

- message enqueue order;
- scheduler steps;
- lease acquisition/takeover;
- crash points;
- adapter responses;
- restart/recovery;
- checkpoint corruption simulation.

Wall-clock timing SHOULD be avoided in conformance tests where a deterministic logical clock/event index can express the scenario.

## 6.33 Conformance evidence package

A runtime conformance claim MUST publish/retain evidence including:

```text
implementation identity/commit
runtime_profile_id
claimed conformance class
store/backend identity/version
adapter identities/versions
golden vector version
pass/fail report
failure-injection report
known exclusions/unsupported guarantees
```

A badge or README statement without this evidence is insufficient.

## 6.34 Reference-profile security limits

RP0 does not by itself guarantee:

- Byzantine fault tolerance;
- globally ordered events;
- exactly-once external effects;
- truthful external services;
- correct application policy;
- legal authorization;
- network availability;
- indefinite liveness;
- fencing on adapters that cannot support a fence token.

These require explicit stronger profiles.

## 6.35 Property targets

- **T-RP0-01 Durable dedup:** committed MessageID consumption survives restart.
- **T-RP0-02 Ack safety:** acknowledged processing corresponds to a committed local durable state transition.
- **T-RP0-03 Authority non-resurrection:** consumed one-shot authority remains consumed after recovery.
- **T-RP0-04 Budget non-amplification:** restart/takeover does not increase remaining budget absent explicit replenishment.
- **T-RP0-05 Receipt-before-dependent-progress:** state dependent on an external outcome references a persisted receipt or explicit UnknownOutcome.
- **T-RP0-06 UnknownOutcome durability:** ambiguous external attempt survives restart until reconciliation.
- **T-RP0-07 Single-active-lease:** within the claimed store domain, stale lease epochs cannot commit exclusive agent state.
- **T-RP0-08 Redelivery equivalence:** duplicate identical messages do not create duplicate durable agent consequences under the declared dedup horizon.
- **T-RP0-09 Checkpoint recoverability:** recovery from a valid checkpoint reconstructs the declared durable frontier.
- **T-RP0-10 Failure-injection closure:** every specified crash point maps to one explicit recoverable state class.

These are obligations, not mechanically proved claims.

## 6.36 Freeze consequence

PRIMA now has one candidate reference runtime profile with explicit storage boundaries, mailbox semantics, transactional acknowledgement, durable dedup/replay/budget state, leases, crash recovery, ambiguous-effect reconciliation, failure injection, conformance classes and evidence requirements.

This converts runtime claims from architecture prose into an executable test program.

**NEXT PRIMA:** §7 Runtime Artifact Identities, Event/Trace Model, and Cross-Runtime Handoff Conformance — bind MessageID/CheckpointID/HandoffID/runtime events to canonical encodings and define portable migration/trace verification across conforming runtimes.