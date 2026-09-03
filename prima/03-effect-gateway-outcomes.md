# PRIMA §3 — Effect Gateway and Outcome Semantics

**Status:** architectural normative draft / freeze candidate

## 3.0 Purpose

The Effect Gateway is the only PRIMA boundary that may convert an authorized finite Plan into privileged external effects under N-0.

```text
Authorized Plan + AuthorizationArtifact + RuntimeContext
    -> EffectGateway
    -> OperationResults + OutcomeReceipt
```

It MUST execute the Plan that was authorized, preserve operation ordering semantics, record observable outcomes, and expose divergence explicitly.

## 3.1 Gateway input

```text
GatewayRequest {
  plan
  authorization_artifact
  runtime_context
  execution_profile
}
```

The request is rejected before effects if any required binding or authority check fails.

## 3.2 Pre-execution validation

Before the first privileged operation, the gateway validates at least:

1. canonical Plan structure under its profile;
2. `PlanID_exec == AuthorizationArtifact.plan_id`;
3. authorization artifact validity/freshness/use policy;
4. runtime principal/domain binding;
5. DecisionCertificate/policy binding carried by the authorization artifact;
6. capability/approval bindings required by the authorization profile;
7. replay/one-shot consumption preconditions;
8. execution-profile support for every operation class.

Failure produces `NotExecuted` with a detailed gateway failure and performs no privileged operation.

## 3.3 Exact-plan invariant

```text
PlanID_exec == PlanID_authorized
```

is mandatory.

The gateway MUST NOT substitute, widen, reinterpret, append, or delete privileged operations after authorization.

Runtime adapters may perform representation-level lowering only if the execution profile defines a verified correspondence to the canonical operation.

## 3.4 Operation execution contract

Each operation class has a profile-defined executor:

```text
Execute_op(op, runtime_context)
   -> OperationResult
```

An executor must declare:

- supported operation class/subset;
- external target/domain;
- request lowering;
- observable result schema;
- expected read/write observation mechanism;
- timeout/cancellation behavior;
- retry/idempotency semantics;
- failure taxonomy;
- security assumptions.

Unsupported operations are rejected; they are not approximated.

## 3.5 Sequential N-0 semantics

Operations execute in canonical Plan order.

For operation sequence `o1...on`, result `ri` is finalized before operation `oi+1` begins unless a future explicit parallel profile applies.

This sequencing is part of the N-0 runtime correspondence contract.

## 3.6 OperationResult

```text
OperationResult {
  op_id
  attempt
  status
  observed_inputs_or_reads[]
  observed_outputs[]
  observed_writes[]
  external_receipts[]
  error?
  timing_context?
}
```

Status begins with:

```text
Succeeded
Failed
Rejected
TimedOut
Cancelled
UnknownOutcome
```

`UnknownOutcome` is required for external systems where the gateway cannot safely determine whether an effect occurred.

## 3.7 Failure policy

The Plan's §1 failure policy governs continuation after an operation result.

### AbortPlan
Stop scheduling later operations after the first non-success result.

### Continue
Record the failure and continue with later operations whose execution remains valid under the Plan/profile.

### Compensate(profile-defined)
Invoke explicit pre-authorized compensating operations according to a compensation profile.

Compensation is a new effect sequence, not time reversal. It may itself fail and MUST be receipted.

## 3.8 Idempotency

Each effect profile declares one of:

```text
NaturallyIdempotent
IdempotentWithKey
NonIdempotent
UnknownIdempotency
```

Retries are permitted only when profile semantics justify them.

For `IdempotentWithKey`, the idempotency key MUST be bound to the canonical Plan/operation identity or an explicitly defined stable derivation.

The gateway MUST NOT blindly retry `NonIdempotent` or `UnknownIdempotency` effects after ambiguous failure.

## 3.9 Retry semantics

A retry is an additional attempt of the same canonical operation, not a new operation.

Every attempt is recorded.

Retry policy declares:

- maximum attempts;
- retryable result/error classes;
- backoff policy as runtime behavior;
- idempotency assumptions;
- whether authorization freshness remains valid across attempts.

Retry scheduling cannot expand the operation's authority or resource scope.

## 3.10 Time and randomness

Gateway execution may use wall-clock time, timers, scheduling, or runtime randomness where the execution profile requires them. These are runtime mechanisms and do not retroactively alter the DFPL semantic Verdict.

Decision-relevant runtime observations needed by a future cycle enter through `OutcomeReceipt`/new evidence.

## 3.11 Observed read/write sets

Where technically observable, the gateway records actual external reads and writes.

```text
ObservedWrites(op) subseteq DeclaredWrites(op)
```

is the default safety expectation.

Privileged writes outside the declared authorized write set produce `Diverged` or a stronger profile-specific failure.

If a backend cannot observe complete writes, the profile MUST state that limitation and MUST NOT claim stronger write-set correspondence than it can verify.

## 3.12 Candidate-state correspondence

After the Plan completes or terminates, the gateway derives/observes a policy-visible actual post-state where the execution profile supports it.

```text
ObservedPostState
```

is compared with the authorized `candidate_transition.post_state` under an explicit equivalence/correspondence relation.

Exact equality is the N-0 default when no profile-defined equivalence exists.

## 3.13 Divergence

`Diverged` occurs when execution materially departs from the authorized Plan or candidate transition, including examples such as:

- undeclared privileged write;
- different target/method/arguments after lowering;
- operation omitted or unexpectedly added;
- actual post-state not equivalent to authorized candidate state;
- executor cannot establish required runtime correspondence.

Divergence is an effect outcome, not a change to the earlier semantic or authorization result.

## 3.14 Partial execution

A Plan may produce external effects before a later failure.

Therefore `Failed` MUST NOT imply `NoEffectOccurred`.

OutcomeReceipt records the exact completed/failed/unknown prefix and any compensation attempts.

Consumers MUST use receipts rather than infer rollback from the final outcome label.

## 3.15 Unknown outcomes

External systems can fail after an effect is submitted but before acknowledgment is observed.

When the gateway cannot determine whether the effect occurred, the operation is `UnknownOutcome`.

The gateway MUST NOT convert uncertainty into `Succeeded` or `Failed` without evidence.

A reconciliation Plan may later query external state and feed the result into a new cycle.

## 3.16 Outcome algebra

Plan-level outcome begins with:

```text
EffectOutcome =
    Executed
  | NotExecuted
  | Diverged
  | Failed
  | PartiallyExecuted
  | UnknownOutcome
```

`Executed` means all required operations completed successfully and required correspondence checks passed.

`NotExecuted` means no privileged operation was performed.

`PartiallyExecuted` means at least one privileged effect occurred but the Plan did not reach the successful terminal condition.

## 3.17 OutcomeReceipt

```text
OutcomeReceiptBody {
  plan_id
  authorization_id
  execution_profile
  runtime_identity
  operation_results[]
  observed_post_state?
  observed_read_set[]
  observed_write_set[]
  compensation_results[]
  outcome
  divergence_detail?
  previous_receipt_ref?
}

OutcomeReceipt {
  receipt_id
  body
  attestation_or_proof?
}
```

`receipt_id` MUST NOT participate in its own content hash.

Exact canonical receipt encoding is a later profile/encoding obligation.

## 3.18 Receipt truth boundary

A receipt establishes only what its execution/attestation profile can support.

A self-reported runtime receipt is not automatically independent proof of execution.

Profiles must distinguish local structured logs, cryptographically authenticated receipts, external transaction receipts, replicated attestations, and stronger proof systems.

## 3.19 Replay consumption

For one-shot authorization, gateway acceptance and replay-state consumption must be coordinated according to the runtime profile so concurrent/repeated requests cannot straightforwardly execute the same authority multiple times.

Atomicity guarantees MUST be stated explicitly; distributed backends may require compare-and-set, transactional storage, ledger sequencing, nonce state, or another defined mechanism.

## 3.20 Runtime correspondence

For an execution profile `τ`, define a lowering/execution/observation relation:

```text
Lower_τ(op) -> request_τ
Execute_τ(request_τ) -> external_result
Observe_τ(external_result, external_state) -> OperationResult
```

The profile must state what it means for the external action to correspond to the canonical operation.

No backend is called conformant merely because it accepted a similarly named API call.

## 3.21 Audit chain

The closed chain is:

```text
PlanID
 -> DecisionCertificate
 -> AuthorizationArtifact
 -> GatewayRequest
 -> OperationResult*
 -> OutcomeReceipt
```

Each artifact binds to the preceding authority/identity objects required by its profile.

## 3.22 Feedback closure

`OutcomeReceipt_n` MAY become explicit `EvidenceIR_{n+1}` after any required verification/normalization step.

This closes:

```text
Observe -> Propose -> Verify -> Authorize -> Act -> Observe
```

without treating requested effects as observed facts.

## 3.23 Theorem/property targets

- **T-GW-01 Exact Plan Binding**: gateway execution implies executed PlanID equals authorized PlanID.
- **T-GW-02 No Unsupported Approximation**: unsupported canonical operations are rejected rather than weakened.
- **T-GW-03 Sequential Correspondence** for N-0 operation order.
- **T-GW-04 Retry Identity**: retries do not change canonical operation identity/scope.
- **T-GW-05 Declared-Write Safety** where the profile claims complete write observation.
- **T-GW-06 Receipt Completeness for Attempts**: every attempted operation/retry/compensation is represented in the receipt.
- **T-GW-07 Partial-Effect Honesty**: final failure never implies no prior effect unless the receipt establishes that fact.
- **T-GW-08 Divergence Separation**: divergence does not mutate prior semantic/authorization artifacts.
- **T-GW-09 One-Shot Replay Safety** under the declared runtime atomicity model.
- **T-GW-10 Receipt Linkage**: receipt binds to exact PlanID and AuthorizationID.

These are obligations, not yet mechanically proved.

## 3.24 Freeze consequence

PRIMA now has a closed candidate runtime-control chain from finite Plan proposal through semantic verification and authorization to external effects and observed outcomes.

**NEXT PRIMA:** §4 Agent, Supervision, and Recursive Process Semantics — how long-running/recursive agents generate finite Plan fragments, handle receipts, retries/recovery, child agents, budgets, and reauthorization without bypassing the Plan/authorization/gateway boundary.
