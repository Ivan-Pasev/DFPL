# PRIMA §4 — Agent, Supervision, and Recursive Process Semantics

**Status:** architectural normative draft / freeze candidate

## 4.0 Purpose

§4 defines how long-running or recursive PRIMA processes generate finite Plan fragments without bypassing DFPL verification, authorization, or the Effect Gateway.

An agent is an orchestration principal/process abstraction. Agent existence or identity never implies authority.

Canonical loop:

```text
Observe
 -> AgentState
 -> GenerateFinitePlan
 -> DFPL-K
 -> Authorization
 -> EffectGateway
 -> OutcomeReceipt
 -> UpdateAgentState
 -> Repeat
```

Each privileged cycle crosses the same PlanID/DecisionCertificate/AuthorizationArtifact boundary as non-agent execution.

## 4.1 Agent identity versus authority

Define distinct concepts:

```text
AgentID
PrincipalID
AuthenticatedPrincipal
CapabilitySet
AgentState
RuntimeProcessIdentity
```

`AgentID` identifies an orchestration entity/lineage. It is not automatically a public key, authenticated principal, capability, legal identity, or operating-system process identity.

## 4.2 Agent descriptor

A canonical agent configuration conceptually contains:

```text
AgentDescriptor {
  agent_id
  parent_agent_id?
  agent_profile
  policy_binding
  principal_binding
  capability_request_policy
  state_schema
  input_channels[]
  output_channels[]
  budget_policy
  supervision_policy
  termination_policy
}
```

Descriptor identity, signing/provenance, and canonical encoding are separate later/profile concerns.

## 4.3 Agent state

Agent runtime state is explicit:

```text
AgentState {
  logical_state
  last_receipt_ref?
  budget_state
  retry_state
  child_refs[]
  supervision_state
}
```

Hidden mutable host state MUST NOT silently influence DFPL-K decisions. Decision-relevant runtime state is surfaced into the next Plan/evidence context.

## 4.4 Finite-plan production rule

A recursive/long-running agent may execute indefinitely as a process, but every authorization unit is one finite canonical PlanIR.

```text
GeneratePlan(agent_state, observations) -> Finite PlanIR
```

A Plan MUST NOT encode an open-ended privileged loop whose future effects cannot be enumerated or bounded by the active authorization/delegation profile.

Unbounded behavior is represented as a sequence of separately authorized finite plans:

```text
P1 -> Receipt1 -> P2 -> Receipt2 -> ...
```

## 4.5 Recursion boundary

PRIMA recursion is orchestration-level recursion, not DFPL-K semantic recursion.

A recursive agent step may call itself/its planner again only after the current cycle reaches a defined orchestration state such as:

- receipt observed;
- authorization rejected;
- retry/recovery decision;
- supervision event;
- explicit wait/termination condition.

No recursive control flow can retroactively mutate a sealed PlanID, LawID, DecisionCertificate, or AuthorizationArtifact.

## 4.6 Observation boundary

Agents consume observations from explicit channels.

Examples:

```text
OutcomeReceipt
verified external event
human message/approval
ledger observation
sensor/tool evidence
supervisor command
scheduled runtime event
```

Observations are not semantic facts until normalized/verified according to the profile that supplies them to a later DFPL Law as state/evidence.

## 4.7 Agent action rule

An agent does not perform a privileged operation merely because its policy/planner selected it.

Agent output is:

```text
Intent -> PlanIR
```

Privileged execution still requires:

```text
PlanIR -> DFPL-K -> DecisionCertificate -> Authorization -> EffectGateway
```

This applies equally to child spawning, messaging, tool calls, writes, deployments, and ledger submissions.

## 4.8 Child agents

`AgentSpawn` is an effect governed by PRIMA §§1–3.

A parent may propose creation of a child descriptor/state, but child existence is recognized only after the spawn operation is observed/receipted by the relevant runtime profile.

Parent-child relation MUST be explicit in lineage/provenance.

## 4.9 Capability inheritance

Children do not automatically inherit all parent authority.

Child effective authority must arise from explicit capability delegation/assignment under PRIMA §2.

Delegated child capabilities obey attenuation-only rules:

```text
rights(child) subseteq rights(parent authority used for delegation)
scope(child) subseteq scope(parent)
validity(child) no broader than parent
constraints(child) equal or stricter
```

Spawning an agent without delegated authority creates an agent that may reason/propose but cannot perform corresponding privileged effects.

## 4.10 Supervision

A supervisor is an orchestration role/process that observes child/process events and emits supervision decisions.

Initial supervision actions:

```text
Continue
Restart
Pause
Resume
Terminate
Escalate
RequestHumanApproval
Replan
SpawnReplacement(profile-defined)
```

Any supervision action requiring privileged external effects becomes a finite Plan and follows normal authorization/gateway semantics.

## 4.11 Supervision tree

N-0 supports an explicit finite supervision graph/tree per runtime snapshot.

Each supervised agent records at most one active immediate supervisor unless a future multi-supervisor profile defines deterministic conflict resolution.

Cycles in the active direct-supervision relation are invalid in N-0.

## 4.12 Restart semantics

`Restart` does not erase history.

A restarted agent receives a new runtime/process incarnation identifier while preserving its AgentID/lineage according to the profile.

The restart policy declares what state is restored:

```text
FreshState
LastCommittedAgentState
StateFromReceipt(ref)
ProfileDefinedCheckpoint(ref)
```

A restart MUST NOT re-execute previously consumed one-shot authorization merely because process memory was lost.

## 4.13 Retry versus replan versus restart

These are distinct:

- **retry** — additional attempt of the same canonical operation under §3 rules;
- **replan** — generate a new PlanIR, requiring new semantic verification/authorization;
- **restart** — replace/reinitialize an agent runtime process under supervision policy.

A restart does not authorize a retry or replan by itself.

## 4.14 Budgets

Agent runtime may be constrained by explicit budgets:

```text
BudgetState {
  max_plan_cycles?
  max_child_agents?
  max_effect_attempts?
  max_compute_units?
  max_runtime_duration?
  max_spend_or_value?
  profile_specific_limits[]
}
```

Budget counters are runtime authority/safety state, not hidden implementation advice.

Where budget exhaustion affects permission, the relevant current budget state must participate in authorization/runtime policy or explicit DFPL evidence as appropriate.

## 4.15 Budget non-amplification

A child/restarted process cannot silently reset or enlarge inherited runtime budgets.

Delegated/replacement budget must be explicitly derived from an available parent/supervisor budget or separately authorized source.

Profiles MUST define accounting conservation/transfer rules for any scarce quantitative budget they claim to enforce.

## 4.16 Agent lifecycle

Initial lifecycle:

```text
Created
Ready
Planning
AwaitingVerification
AwaitingAuthorization
AwaitingExecution
AwaitingObservation
Paused
Recovering
Terminating
Terminated
Failed
```

The lifecycle is orchestration state, not DFPL Verdict state.

Transitions requiring external effects still pass through Plan/authorization/gateway boundaries.

## 4.17 Receipt-driven progression

An agent MUST NOT treat requested or submitted effects as successful observations.

State progression that depends on effects uses `OutcomeReceipt` or profile-defined verified observation.

Thus:

```text
PlanSubmitted != EffectSucceeded
AuthorizationGranted != EffectSucceeded
EffectRequestSent != EffectSucceeded
```

## 4.18 UnknownOutcome handling

If an operation/Plan yields `UnknownOutcome`, the agent MUST NOT simply assume success/failure for subsequent decision-relevant state.

Allowed orchestration responses include:

- pause;
- reconcile/query external state;
- escalate;
- generate a separate recovery Plan;
- await verified observation.

Blind re-execution is prohibited unless the execution profile proves it safe through idempotency/replay semantics.

## 4.19 Failure and recovery

Agent-level failure categories remain distinct from semantic, authorization, and effect failures.

Conceptually:

```text
PlanningFailure
VerificationFailure
AuthorizationFailure
ExecutionFailure
ObservationFailure
SupervisionFailure
BudgetExhausted
RecoveryFailed
TerminalAgentFailure
```

Recovery policy maps these events to supervision/orchestration actions without rewriting the underlying DFPL Verdict/AuthorizationResult/OutcomeReceipt.

## 4.20 Persistent loops

A long-running agent loop is modeled as repeated finite state transitions:

```text
A_n + Obs_n
 -> Plan_n
 -> Verdict_n
 -> Auth_n
 -> Receipt_n
 -> A_(n+1)
```

The loop itself is not one indefinitely valid authorization object.

A bounded delegated-authority profile MAY authorize a class of future plans only if its scope, constraints, replay/use policy, and verification semantics are explicitly defined; N-0 assumes per-Plan authorization.

## 4.21 Event ordering

For each agent, N-0 defines a deterministic logical processing order over the events admitted to one planning step.

The runtime profile MUST define how concurrently arriving events are converted into a deterministic ordered input batch or explicit unordered canonical collection.

Host thread scheduling MUST NOT silently define semantic planning order where that order affects canonical Plan generation.

## 4.22 Deterministic versus nondeterministic planners

PRIMA does not require all planners/agents to be deterministic.

A nondeterministic or stochastic planner may propose different Plans from the same observations, but every produced Plan has a finite canonical PlanID and independently crosses the verification/authorization boundary.

Randomness affecting a DFPL semantic decision is still explicit evidence/state; planner randomness alone does not modify DFPL-K semantics.

## 4.23 Model/LLM agents

An LLM/model may serve as a planner, classifier, generator, critic, or supervisor component.

Model output is untrusted orchestration input until converted to canonical PlanIR/evidence under the applicable boundary.

A model MUST NOT be treated as an authorization oracle merely because it emits natural-language approval or claims that policy passed.

Model/provider/version/context metadata SHOULD be captured where needed for reproducibility/audit but does not automatically become semantic Law input.

## 4.24 Tool calls

Tool invocation requested by an agent is an effect operation unless explicitly classified as pure/internal by a profile.

External tool results are observations/receipts whose trust level matches the tool/runtime attestation profile.

A tool call name is not proof that the external operation corresponding to that name occurred.

## 4.25 Agent lineage and provenance

Agent descriptors/incarnations SHOULD record lineage/provenance references sufficient to reconstruct:

- parent/supervisor relationship;
- descriptor version;
- relevant source/model/runtime version;
- policy/kernel bindings;
- capability delegation provenance;
- prior checkpoint/receipt lineage.

These are audit/provenance data unless explicitly represented as semantic state/evidence.

## 4.26 Termination

Agent termination may occur because of:

- explicit terminal policy;
- supervisor termination;
- budget exhaustion;
- unrecoverable failure;
- human/operator decision;
- completed objective/profile condition.

A terminated agent cannot perform new privileged effects without a separately defined reactivation/new-incarnation process and fresh applicable authority.

## 4.27 No immortal authorization

No agent identity, descriptor, long-lived process, or supervision relationship grants indefinite universal execution authority.

Authority remains bounded by the capabilities, approvals, validity, replay/use policy, and Plan binding defined in PRIMA §2/§3.

## 4.28 Safety invariants

- **PRIMA-A001 Finite Plan Boundary** — every privileged agent cycle yields a finite PlanIR.
- **PRIMA-A002 Authority Separation** — AgentID/existence does not imply authority.
- **PRIMA-A003 Child Attenuation** — child delegated authority cannot exceed its valid parent delegation chain.
- **PRIMA-A004 Receipt-Driven Effects** — requested/submitted effects are not treated as observed success without receipt/verified observation.
- **PRIMA-A005 Restart Non-Replay** — process restart does not reset consumed one-shot authority.
- **PRIMA-A006 Budget Explicitness** — enforced agent budgets are explicit runtime state.
- **PRIMA-A007 UnknownOutcome Honesty** — uncertainty remains explicit until reconciled.
- **PRIMA-A008 Supervision Separation** — supervision actions do not mutate prior semantic/authorization/effect artifacts.
- **PRIMA-A009 Replan Reauthorization** — materially new PlanIR requires fresh verification/authorization.
- **PRIMA-A010 No Immortal Authority** — persistent identity/process does not grant unlimited future effect authority.

## 4.29 Theorem/property targets

- **T-AGENT-01 Finite Authorization Units** — every privileged agent execution is attributable to one finite authorized PlanID.
- **T-AGENT-02 Child Authority Non-Amplification** under valid delegation.
- **T-AGENT-03 Receipt Progression** — any agent state transition claiming effect success is backed by a qualifying receipt/observation under its profile.
- **T-AGENT-04 Restart Replay Safety** — restart cannot make a consumed one-shot authorization valid again under the declared runtime model.
- **T-AGENT-05 Replan Identity Separation** — materially changed canonical Plan produces a fresh PlanID/authorization cycle.
- **T-AGENT-06 Supervision Acyclicity** for N-0 active direct-supervision graph.
- **T-AGENT-07 Budget Non-Amplification** under parent/child/restart allocation rules where quantitative budgets are enforced.
- **T-AGENT-08 UnknownOutcome Safety** — unknown external outcome is not converted into success/failure without qualifying evidence.
- **T-AGENT-09 Semantic Artifact Immutability** — agent/supervisor transitions cannot mutate sealed Kernel/Law/Decision artifacts.

These are obligations, not yet mechanically proved.

## 4.30 Freeze consequence

PRIMA now has a candidate long-running agent model that preserves the finite Plan/verification/authorization/effect/receipt boundary across recursion, child agents, supervision, restart, recovery, budgets, LLM planners, and persistent loops.

**NEXT PRIMA:** §5 Runtime Profiles, Messaging, Scheduling, and Agent State Persistence — canonical profile requirements for event transport, durable checkpoints, mailbox/order semantics, leases/ownership, cross-runtime handoff, and profile conformance.
