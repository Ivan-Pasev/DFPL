# PRIMA §1 — PlanIR and Effect Algebra

**Status:** architectural normative draft / freeze candidate

## 1.0 Purpose

PlanIR is the finite canonical representation of proposed effectful intent before authorization or execution.

`Intent → PRIMA → PlanIR → CandidateTransition + EvidenceIR → DFPL-K → DecisionCertificate → Authorization → EffectGateway`

A Plan describes what is proposed. It is not authority to act.

## 1.1 Identity split

```text
PlanIRBody {
  principal
  domain
  operations[]
  declared_inputs[]
  expected_outputs[]
  candidate_transition
  policy_binding
  evidence_binding
  capability_requirements[]
  replay_context
}

PlanArtifact {
  plan_id
  body
}
```

`plan_id` MUST NOT appear inside the bytes used to calculate itself.

Candidate:

`PlanID = H(DS_PLAN || CanonicalPlanEncode(PlanIRBody))`

Exact encoding is a future canonicalization obligation.

## 1.2 Principal

`principal` identifies the runtime actor on whose behalf the plan is proposed. Principal identity does not itself prove authentication, capability possession, or legal authority.

## 1.3 Domain

`domain` scopes operation semantics and authorization context. It prevents equal-looking operations in different execution domains from being silently conflated.

## 1.4 Operation algebra

Initial operation classes:

```text
PureCompute
ReadState
FileRead
FileWrite
NetworkRead
NetworkWrite
ToolInvoke
MessageSend
AgentSpawn
LedgerRead
LedgerSubmit
ArtifactCreate
ArtifactDeploy
TimeRead
RandomnessRead
HumanApproval
```

Profiles MAY refine these classes but MUST NOT silently weaken their authorization or audit requirements.

## 1.5 Operation structure

Each operation is finite and typed, conceptually:

```text
Operation {
  op_id
  class
  target
  arguments
  declared_reads[]
  declared_writes[]
  required_capabilities[]
  expected_result_type
  failure_policy
}
```

Operation IDs MUST be unique within a Plan.

## 1.6 Reads and writes

Every operation that observes or changes external state SHOULD declare a conservative read/write set.

An implementation MAY discover that an operation touched less state than declared. Touching undeclared privileged state is divergence or execution failure unless a profile explicitly defines a safe widening rule.

## 1.7 Sequencing

Plan operations execute in canonical sequence order. N-0 PlanIR uses explicit sequential ordering rather than implicit host scheduling.

Parallelism may be introduced by a future profile only with defined dependency, determinism, conflict, and receipt semantics.

## 1.8 Candidate transition

The plan MUST expose either:

1. explicit `pre_state` and candidate `post_state`; or
2. a deterministic adapter that derives the policy-visible candidate transition from the Plan.

The DFPL semantic kernel evaluates this candidate transition; it does not execute it.

## 1.9 Policy binding

```text
PolicyBinding {
  kernel_id
  law_ids[]
  policy_profile
}
```

The authorization path MUST bind to the exact Kernel/Law set evaluated.

Runtime substitution with a weaker policy after verification is forbidden.

## 1.10 Evidence binding

PlanIR references the EvidenceIR required by the bound policy.

Raw claims and verified evidence are distinct. Authenticity/verification is performed by the applicable evidence profile/gateway before semantic consumption where required.

## 1.11 Capability requirements

Capabilities are explicit nominal authority objects, not strings or addresses.

A Plan states capabilities required for each privileged operation. Authorization verifies possession/scope independently of DFPL semantic Permit.

## 1.12 Replay context

Replay-sensitive plans MUST declare enough context to support authorization policy such as:

- nonce/sequence,
- freshness window,
- domain,
- previous receipt or state commitment,
- one-shot/reusable classification.

The core architecture does not assume that a timestamp alone prevents replay.

## 1.13 Failure policy

Initial operation failure policies:

```text
AbortPlan
Continue
Compensate(profile-defined)
```

`Compensate` is not rollback by magic. A compensation profile must define explicit compensating operations and failure semantics.

## 1.14 Finite-plan rule

Each authorized PlanIR MUST be finite.

A recursive or persistent agent may generate an unbounded sequence:

`P1, P2, P3, ...`

but each authorization binds to one finite plan fragment unless a future capability profile explicitly defines bounded delegated authority.

## 1.15 Plan mutation

If canonical PlanIR changes after authorization, its PlanID changes and a fresh verification/authorization cycle is required.

`PlanID_exec == PlanID_authorized`

is a mandatory Effect-Gateway invariant.

## 1.16 Authorization layering

Three layers remain distinct:

Semantic verdict:
`Permit / Deny / PreconditionFailure / PostconditionFailure / Invalid`

Authorization decision:
`Authorized / NotAuthorized / ApprovalRequired`

Effect outcome:
`Executed / NotExecuted / Diverged / Failed`

`Permit != Authorized != Executed`.

## 1.17 OutcomeReceipt correspondence

An attempted privileged execution SHOULD emit:

```text
OutcomeReceipt {
  plan_id
  authorization_id
  operation_results[]
  observed_post_state
  observed_write_set
  outcome
  runtime_identity
  receipt_commitment
}
```

A receipt records observed execution facts under a profile; it does not retroactively alter the semantic verdict.

## 1.18 Divergence

If actual operations, writes, or observed post-state differ materially from the authorized Plan/candidate transition, the result is `Diverged` unless a profile defines and verifies an allowed equivalence/refinement relation.

## 1.19 Effect Gateway obligations

Before execution the gateway validates at least:

- PlanID,
- policy binding,
- DecisionCertificate,
- authorization decision,
- principal,
- capabilities,
- domain,
- replay/freshness constraints.

No privileged operation may rely solely on an agent's assertion that it was permitted.

## 1.20 Theorem/property targets

- **PLAN-01 Identity stability:** equal canonical PlanIRBody gives equal PlanID under the selected encoding/hash assumptions.
- **PLAN-02 Mutation separation:** material canonical plan changes produce a distinct PlanIR body/identity.
- **PLAN-03 Authorization binding:** an authorization refers to exactly one PlanID and policy binding.
- **PLAN-04 Execution binding:** an execution accepted by the gateway uses the authorized PlanID.
- **PLAN-05 Finite authorization:** every authorized N-0 plan contains finitely many operations.
- **PLAN-06 Receipt linkage:** OutcomeReceipt binds to the Plan/authorization it reports.

These are obligations, not yet mechanically proved.

## 1.21 Freeze consequence

PRIMA now has a canonical object separating recursive intent generation from privilege-bearing execution.

**NEXT PRIMA:** §2 Capability and Authorization Model.
