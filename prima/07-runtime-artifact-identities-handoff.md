# PRIMA §7 — Runtime Artifact Identities, Event/Trace Model, and Cross-Runtime Handoff Conformance

**Status:** Freeze candidate — 2026-09-04

## Purpose
§7 defines stable runtime artifact identities and a portable audit/handoff model so persistent PRIMA agents may restart or migrate without confusing transport metadata, causal trace, durable state, authority or effect evidence.

## Identity principle
Runtime IDs are content identities over canonical bodies and exclude their own identity fields. `Identity != authenticity != authority != successful processing`. Artifact-family domain separation is mandatory.

## MessageID
`MessageBody` binds runtime profile, sender/target, message type, payload/commitment, correlation/causation and optional logical-order/auth commitments.

`MessageID = SHA256("PRIMA-MESSAGE-v1\0" || RuntimeProfileID || CanonicalEncode(MessageBody))`.

Delivery attempt, broker offset, receive time and transport headers are non-identity metadata unless a profile explicitly promotes them. Redelivery retains MessageID.

## CheckpointID
CheckpointBody contains durable AgentState and the mailbox/dedup, replay/authority, budget, receipt, UnknownOutcome, profile and lease frontiers defined by §§5–6.

`CheckpointID = SHA256("DFPL-CHECKPOINT-v1\0" || RuntimeProfileID || CanonicalEncode(CheckpointBody))`.

Checkpoint identity does not prove external effects.

## RuntimeEvent / EventID
`RuntimeEventBody {runtime_profile_id,event_kind,agent_id,incarnation_id,subject_ref,payload_or_commitment,causation_event_ids[],correlation_id?,logical_order_context?,lease_epoch?,previous_event_ref?}`.

`EventID = SHA256("PRIMA-EVENT-v1\0" || RuntimeProfileID || CanonicalEncode(RuntimeEventBody))`.

Initial kinds cover message delivery/ack, local commits, Plan/Decision/Authorization observations, execution intent/attempt, receipts, UnknownOutcome/reconciliation, checkpoint/lease/handoff and lifecycle events. Event records inherit only the assurance of their backing artifacts/profile.

## Trace model
A Trace is a finite EventID DAG. Causation is explicit; correlation is not causation. Wall-clock coincidence does not define order. Multiple topological orders may be valid when a profile does not provide total order. Trace identity is audit identity, not DFPL semantic identity.

Canonical audit linkage may connect:

`MessageID -> PlanID -> DecisionID -> AuthorizationID -> Attempt -> ReceiptID -> CheckpointID -> HandoffID`.

Each artifact is independently verified under its owning specification.

## RuntimeHandoff
`RuntimeHandoffBody` binds handoff profile, AgentID, source/target runtime/incarnation classes, CheckpointID/commitment, mailbox/dedup/replay-authority/budget/receipt frontiers, pending UnknownOutcome set, lease transition, authority revalidation, trace frontier and compatibility claim.

`HandoffID = SHA256("PRIMA-HANDOFF-v1\0" || HandoffProfileID || CanonicalEncode(RuntimeHandoffBody))`.

## Prepare / accept
PrepareHandoff quiesces or fences the source as required, commits final state/frontiers and emits the handoff artifact. AcceptHandoff validates identity, profile, checkpoint, target compatibility, security frontiers, unresolved effects and lease transition before activating a new incarnation. Privileged work cannot begin before required fencing and authority revalidation.

## Runtime compatibility
`RuntimeCompat(source_profile,target_profile,handoff_profile,supported_domain)` is directional. Initial classes:

`ExactState | RecoveryEquivalent | SafetyRefinement | ObservationOnly | Incompatible`.

A target may provide weaker liveness/performance while preserving declared safety; it may not inherit stronger delivery/fencing/durability/effect guarantees without evidence.

## Safety invariants
- consumed authority remains consumed;
- budgets do not increase absent explicit new policy;
- known receipt frontier is monotone;
- unresolved UnknownOutcome survives;
- required dedup horizon survives;
- stale source is fenced where claimed;
- AgentID continuity does not imply IncarnationID continuity.

`HandoffPrepared != HandoffAccepted != SourceRetired`.

Failed/partial handoff must enter explicit recovery states rather than silent dual activity.

## Trace privacy
Portable traces should use commitments/references for sensitive payloads. Redaction cannot mutate canonical artifact bodies while retaining the same ID. Selective-disclosure/proof profiles remain separate extensions.

## Required vectors
Stable MessageID under redelivery; payload mutation; checkpoint frontier sensitivity; causal DAG reproduction; crash during prepare; stale source after lease transfer; premature target activation rejection; authority/budget/receipt/UnknownOutcome preservation; incompatible target rejection; exact/recovery-equivalent migration; handoff tamper/replay; concurrent incomparable trace events.

Cross-runtime conformance requires executable evidence on both source and target; serialization success alone is insufficient.

## Security limits
Artifact hashes do not authenticate principals. Handoff requires explicit authentication/trust profiles. It does not provide Byzantine consensus, truthful global time, external-service correctness or exactly-once external effects.

## Property targets
T-HAND-01 Message Identity Stability; T-HAND-02 Artifact Domain Separation; T-HAND-03 Causal Edge Preservation; T-HAND-04 Authority Non-Resurrection; T-HAND-05 Budget Non-Amplification; T-HAND-06 Receipt Frontier Monotonicity; T-HAND-07 UnknownOutcome Preservation; T-HAND-08 Dedup Horizon Preservation; T-HAND-09 Lease/Fencing Handoff Safety where claimed; T-HAND-10 Cross-Runtime Compatibility Soundness.

These remain obligations until evidenced.

## Freeze consequence
PRIMA now has a candidate portable identity and migration/audit contract from message delivery through Plan/Decision/Authorization/Receipt to checkpoint and cross-runtime handoff.

## NEXT
§8 — RP0 Machine-Readable Event/Handoff Corpus and Reference Runtime Execution Evidence.