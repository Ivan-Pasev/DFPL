# PRIMA §5 — Runtime Profiles, Messaging, Scheduling, and Agent State Persistence

**Status:** architectural normative draft / freeze candidate

## 5.0 Purpose

PRIMA §5 defines how persistent/recursive agents survive real runtime conditions without weakening the Plan → Decision → Authorization → EffectGateway → OutcomeReceipt chain.

The runtime may schedule, pause, resume, migrate, retry, restart, or recover agents, but these mechanisms MUST NOT silently redefine DFPL semantics, Plan identity, authority, replay policy, or receipt history.

## 5.1 Runtime profile

A runtime profile declares at least:

```text
RuntimeProfile {
  runtime_profile_id
  message_transport
  mailbox_semantics
  scheduler_semantics
  persistence_semantics
  lease/ownership_semantics
  checkpoint_semantics
  recovery_semantics
  authentication_semantics
  time/freshness_semantics
  receipt_store_semantics
  resource/budget_semantics
}
```

A profile is a claim boundary. It MUST state exactly what ordering, durability, delivery, replay, failure, and recovery guarantees it provides.

## 5.2 Agent incarnation

Persistent logical agent identity is distinct from one running process instance.

```text
AgentIncarnation {
  agent_id
  incarnation_id
  runtime_profile_id
  lease_epoch?
  checkpoint_ref?
}
```

`agent_id` identifies the logical agent lineage. `incarnation_id` identifies one runtime incarnation.

Restart or migration creates a new incarnation unless the runtime profile explicitly defines a stronger continuity object.

## 5.3 Mailbox model

Every persistent agent receives canonical message envelopes through a mailbox abstraction.

```text
MessageEnvelope {
  message_id
  sender_principal?
  target_agent_id
  message_type
  payload
  correlation_id?
  causation_id?
  delivery_attempt
  authentication_context?
  ordering_context?
}
```

Message payloads are data. Receipt of a message does not itself authorize an effect.

## 5.4 Message identity and deduplication

`message_id` MUST be stable across redelivery of the same logical message.

A runtime profile declaring deduplication semantics MUST define:

- deduplication key;
- retention horizon;
- persistence scope;
- behavior across restart/migration;
- interaction with mailbox acknowledgement.

Duplicate delivery MUST NOT silently create duplicate authority or bypass one-shot authorization controls.

## 5.5 Delivery guarantees

A transport/profile MUST identify its guarantee class, for example:

```text
BestEffort
AtMostOnce
AtLeastOnce
EffectivelyOnce(profile-defined)
```

PRIMA does not use the phrase `ExactlyOnce` unless the profile defines the exact scope and proves/establishes the required atomicity across message consumption and resulting durable effects/state transitions.

`AtLeastOnce` delivery requires idempotent/deduplicated handling where duplicate consequences would be unsafe.

## 5.6 Ordering

A runtime MUST NOT claim global message order unless it provides and verifies it.

Ordering may be scoped as:

```text
None
PerSender
PerAgentMailbox
PerPartition
Causal(profile-defined)
Total(profile-defined)
```

An agent decision depending on ordering must derive that order from explicit message/sequence state supported by the profile, not from incidental host scheduling.

## 5.7 Acknowledgement boundary

Mailbox acknowledgement is separate from effect success.

A message MAY be acknowledged:

- after durable enqueue to agent state;
- after successful Plan construction;
- after OutcomeReceipt persistence;
- according to another explicit profile rule.

The profile MUST define the acknowledgement point because it determines redelivery/recovery behavior.

## 5.8 Scheduler semantics

The scheduler selects runnable agent incarnations/events. Scheduler choice is runtime mechanism, not DFPL semantic input unless explicitly reflected into agent state/evidence.

A profile declares:

- fairness claim, if any;
- priority semantics;
- starvation behavior;
- scheduling quanta/budgets;
- concurrency model;
- cancellation semantics;
- timer handling.

No correctness theorem may rely on unspecified scheduler fairness.

## 5.9 Timers and time

Timers are runtime events, not hidden DFPL-K clocks.

A timer event delivered to an agent is represented explicitly, e.g.:

```text
TimerEvent {
  timer_id
  scheduled_context
  observed_fire_context
}
```

If semantic policy depends on time, an explicit trusted/attested time value must enter the applicable Law evidence/state. Runtime timer firing alone does not retroactively change a previous Verdict.

## 5.10 Durable agent state

Persistent agent state is an explicit versioned object separate from process memory.

```text
AgentState {
  agent_id
  state_schema_id_or_profile
  state_version
  logical_state
  consumed_message_state
  budget_state
  pending_plan_refs[]
  pending_reconciliation_refs[]
  last_receipt_refs[]
  supervisor_ref?
}
```

Ephemeral caches may exist but MUST NOT be required to reconstruct normative/runtime authority state unless the profile explicitly declares them durable.

## 5.11 Checkpoints

A checkpoint is a durable snapshot suitable for recovery under one runtime profile.

```text
CheckpointBody {
  agent_id
  incarnation_id
  agent_state
  mailbox_cursor_or_delivery_state
  replay/authorization consumption state
  budget_state
  receipt_frontier
  runtime_profile_id
}

Checkpoint {
  checkpoint_id
  body
  attestation?
}
```

`CheckpointID` follows the §8-style domain-separated canonical identity pattern defined by the applicable profile.

A checkpoint does not prove that all external effects described by local state actually occurred; OutcomeReceipts remain the execution evidence boundary.

## 5.12 Checkpoint consistency

A runtime profile MUST state its checkpoint consistency model, including whether agent state, mailbox acknowledgement state, authorization/replay consumption state, and receipt references are captured atomically.

If they are not atomic, recovery MUST define reconciliation behavior rather than assuming impossible consistency.

## 5.13 Lease / ownership semantics

Distributed runtimes SHOULD prevent uncontrolled concurrent active incarnations of one exclusive agent authority domain using a lease/epoch/fencing mechanism.

Conceptually:

```text
Lease {
  agent_id
  holder_incarnation_id
  lease_epoch
  validity_context
}
```

A new lease epoch fences stale incarnations under the profile's external-state/effect adapters where such fencing is supported.

A lease is not itself a capability to perform arbitrary effects; it is runtime ownership coordination.

## 5.14 Split-brain honesty

If the runtime cannot prevent or detect concurrent active incarnations, the profile MUST state this limitation.

It MUST NOT claim single-writer/exclusive-agent semantics without an enforceable mechanism.

Where split brain is detected, affected effects/state transitions enter reconciliation/divergence handling rather than being silently merged.

## 5.15 Pause and resume

Pause stops new agent progression according to the runtime profile. It does not revoke already externalized effects.

Resume continues from explicit durable state/checkpoint and current authority/freshness conditions.

Expired/revoked capabilities or authorizations are revalidated as required; resume does not make old authority immortal.

## 5.16 Restart

Restart creates/restores an agent incarnation from durable state.

Restart MUST preserve:

- consumed-message/dedup state according to profile guarantees;
- used one-shot authorization/replay state;
- receipt history/frontier;
- budget consumption;
- pending UnknownOutcome reconciliation work.

Restart MUST NOT reset these merely because process memory was lost.

## 5.17 Migration / cross-runtime handoff

Migration moves logical agent execution between runtime instances/profiles.

A handoff artifact conceptually binds:

```text
RuntimeHandoff {
  agent_id
  source_incarnation
  source_runtime_profile
  target_runtime_profile
  checkpoint_id
  lease/fencing transition
  mailbox/delivery frontier
  receipt frontier
  pending unknown outcomes
  authority revalidation requirements
}
```

The target MUST NOT claim guarantees stronger than either the handoff evidence or its own profile supports.

## 5.18 Recovery

Recovery begins from the latest profile-valid durable state and must reconcile ambiguous external effects before blindly replaying non-idempotent operations.

Required recovery questions include:

1. Which messages may be redelivered?
2. Which Plan/authorization artifacts were already consumed?
3. Which operations have confirmed receipts?
4. Which operations are `UnknownOutcome`?
5. Which budgets were already spent?
6. Which lease epoch is current?

Unknown answers remain explicit uncertainty.

## 5.19 UnknownOutcome persistence

`UnknownOutcome` is durable recovery state.

It MUST survive restart/migration until reconciled or explicitly abandoned under a profile-defined rule.

A recovered agent MUST NOT simply regenerate the same non-idempotent effect as a new Plan without considering the unresolved prior effect.

## 5.20 Messaging authentication

A runtime profile defines how message authenticity/integrity is represented, for example local trusted transport, signed envelopes, mTLS/workload identity, ledger messages, or other mechanisms.

`sender_principal` is not trusted merely because a payload contains a name/string.

Authenticated message identity still does not imply capability/authorization for requested effects.

## 5.21 Correlation and causation

`correlation_id` groups related workflow events. `causation_id` references the event/receipt/message that caused another event where known.

These fields improve traceability but do not by themselves establish semantic correctness.

A canonical trace can therefore follow:

```text
Message -> Plan -> Decision -> Authorization -> OutcomeReceipt -> Message/State
```

## 5.22 Event sourcing profile

A runtime MAY represent AgentState as a fold over durable events.

If so, the profile MUST freeze:

- event schema/versioning;
- event ordering scope;
- deduplication rules;
- snapshot/checkpoint relation;
- migration rules;
- replay determinism boundaries;
- treatment of external OutcomeReceipts.

Event sourcing is a profile, not a universal PRIMA requirement.

## 5.23 State schema evolution

Persistent agent state schema changes require explicit migration.

```text
MigrateState(profile, version_a, state_a) -> version_b, state_b
```

Migration MUST preserve or explicitly transform replay state, authority consumption, budgets, pending reconciliation, and receipt linkage.

A failed migration does not authorize dropping security-critical state.

## 5.24 Budget persistence

Budgets/quotas consumed by agent operation are durable where they govern safety/resource authority.

Restart, migration, child creation, or replay MUST NOT replenish a budget unless an explicit policy/authorization does so.

## 5.25 Supervision persistence

Supervisor/child relations that matter to authority/recovery are persistent state.

If a supervisor is lost, child agents do not automatically gain independence or broader capability. Reparenting/recovery requires explicit runtime/policy handling.

## 5.26 Runtime receipt store

The profile defines durable storage/retrieval for OutcomeReceipts and related execution artifacts, including retention, integrity/authentication, indexing, and failure behavior.

An agent state entry saying `operation succeeded` is not a substitute for the applicable execution receipt when the system claim depends on that receipt.

## 5.27 Concurrency

Concurrent agent processing is allowed only under profile-defined mailbox/state concurrency rules.

For one logical agent, candidate models include:

```text
SingleThreadedMailbox
OptimisticVersionedState
PartitionedState
ActorReentrancy(profile-defined)
```

State conflicts must be detected/resolved explicitly. Host-level races are not accepted as semantics.

## 5.28 Backpressure

Runtime profiles SHOULD define mailbox/resource backpressure behavior:

- maximum queue depth;
- rejection/drop semantics;
- producer throttling;
- priority behavior;
- dead-letter handling;
- overload receipt/telemetry.

Dropping an authenticated command/message silently may violate higher-level guarantees and must match the profile's declared behavior.

## 5.29 Dead letters and poison messages

Repeatedly unprocessable messages may move to a dead-letter/review state under explicit policy.

This does not count as successful processing. Dead-letter status must be observable and auditable where the message has operational significance.

## 5.30 Runtime profile conformance

A runtime profile conformance suite SHOULD include:

- duplicate message delivery;
- out-of-order delivery;
- restart between message receipt and acknowledgement;
- restart between authorization and effect;
- crash after external submit before receipt observation;
- concurrent lease contenders;
- stale incarnation fencing;
- checkpoint corruption/missing checkpoint;
- state migration failure;
- UnknownOutcome reconciliation;
- budget persistence across restart;
- mailbox overload/backpressure;
- replay of one-shot authorization after recovery.

## 5.31 Theorem/property targets

- **T-RUN-01 Dedup safety** under the declared retention/persistence model.
- **T-RUN-02 Restart replay safety** for consumed one-shot authority.
- **T-RUN-03 Budget persistence**: restart/migration does not amplify remaining budget.
- **T-RUN-04 Checkpoint linkage**: restored state corresponds to one declared checkpoint/profile state.
- **T-RUN-05 Receipt frontier preservation** across restart/migration.
- **T-RUN-06 UnknownOutcome persistence** until explicit reconciliation.
- **T-RUN-07 Lease fencing safety** where exclusive ownership is claimed.
- **T-RUN-08 Message-auth separation**: authenticated sender identity does not imply effect authorization.
- **T-RUN-09 State migration safety** for security-critical replay/authority fields.
- **T-RUN-10 Scheduler non-interference**: incidental host scheduling does not mutate sealed DFPL semantic artifacts.

These are obligations, not mechanically proved claims.

## 5.32 Freeze consequence

PRIMA now has a candidate durable-runtime model for messages, scheduling, checkpoints, leases, restart, migration, recovery, budget continuity, receipt continuity, and uncertain external outcomes without bypassing finite Plan authorization.

**NEXT PRIMA:** §6 Runtime Conformance and Reference Profile — define one minimal executable runtime profile, test vectors, durable store/mailbox semantics, failure injection matrix, and correspondence requirements suitable for a reference implementation.
