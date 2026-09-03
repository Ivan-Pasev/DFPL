# PRIMA §2 — Capability and Authorization Model

**Status:** architectural normative draft / freeze candidate

## 2.0 Purpose

This section defines the runtime authority layer between a DFPL semantic verdict and privileged execution.

`DecisionCertificate + PrincipalAuth + Capabilities + Approvals + RuntimeContext -> AuthorizationDecision`

Semantic Permit is necessary only where the bound policy requires it; it is never sufficient by itself to execute an effect.

## 2.1 Separation of identities

The model distinguishes:

- PrincipalID — runtime actor namespace;
- AuthenticationEvidence — evidence that a runtime actor controls/represents a PrincipalID;
- Capability — scoped authority to request/perform classes of effects;
- Approval — explicit authorization contribution from an approver/policy;
- AuthorizationArtifact — decision binding all required authority context to one PlanID;
- LegalIdentity — external legal concept, connected only through explicit attestations/profiles.

No one identifier silently substitutes for another.

## 2.2 Capability identity split

Capability semantic body and identity/envelope are distinct:

```text
CapabilityBody {
  issuer
  subject
  domain
  rights[]
  resource_scope
  constraints[]
  valid_from?
  valid_until?
  delegation
  revocation_ref?
}

CapabilityArtifact {
  capability_id
  body
  authentication_or_attestation
}
```

`capability_id` MUST NOT be inside the bytes used to calculate itself.

Candidate:

`CapabilityID = H(DS_CAP || CanonicalCapabilityEncode(CapabilityBody))`

Exact byte encoding and cryptographic envelope remain profile/encoding work.

## 2.3 Rights and resource scope

A capability grants explicitly enumerated right classes over an explicitly represented resource scope.

Examples:

```text
File.Read(path-prefix)
File.Write(path-prefix)
Network.Request(origin/method constraints)
Tool.Invoke(tool-id, operation-set)
Message.Send(channel/recipient scope)
Agent.Spawn(agent-profile scope)
Ledger.Submit(network/contract/method scope)
Artifact.Deploy(target/environment scope)
```

Absence of a right means no authority for that right.

## 2.4 Least-authority coverage

Authorization for Plan `P` requires every privileged operation to be covered by sufficient effective capabilities.

For each operation `op`:

`RequiredAuthority(op) subseteq EffectiveAuthority(AuthContext)`

If any operation is uncovered, the Plan cannot be `Authorized`.

Capabilities may cover multiple operations, but excess capability is not inferred or expanded from use.

## 2.5 Constraints

Capability constraints may restrict:

- target/resource selector;
- operation/method;
- argument ranges;
- amount/quantity limits;
- domain/environment;
- time/freshness interval;
- maximum uses;
- required co-approval;
- required policy/kernel/law binding;
- allowed Plan class/profile.

Constraint evaluation belongs to authorization, not DFPL semantic evaluation, unless a Law explicitly imports the same fact as semantic evidence.

## 2.6 Delegation

Delegation is explicit and attenuation-only.

A delegated child capability MUST NOT grant authority broader than its parent chain.

For child `C2` delegated from parent `C1`:

- rights(C2) ⊆ rights(C1);
- resource_scope(C2) ⊆ resource_scope(C1);
- validity(C2) is no broader than validity(C1);
- constraints(C2) are equal or stricter;
- delegation depth/budget decreases according to the parent rule.

Authority amplification through delegation is invalid.

## 2.7 Delegation chain validation

A delegated capability is effective only when the entire declared chain validates under the active capability profile:

1. identities/links are well-formed;
2. each delegation is authenticated/attested as required;
3. each child attenuates its parent;
4. no capability is expired under the supplied authorization-time context;
5. revocation checks required by the profile are satisfied;
6. the final subject matches the authenticated principal or an explicitly allowed representation relation.

## 2.8 Authentication boundary

`PrincipalID` alone never proves who is acting.

Authorization receives an `AuthenticatedPrincipal` or equivalent profile-defined object produced by an authentication gateway:

```text
AuthenticatedPrincipal {
  principal_id
  authentication_profile
  evidence_commitment
  assurance_context
}
```

PRIMA §2 does not prescribe one universal authentication technology. Passwords, passkeys, hardware keys, workload identity, multisig, delegated service identity, or other systems belong to profiles.

## 2.9 Approval model

Some plans require explicit approval beyond capability possession.

An approval binds at minimum to:

- approver/approval authority;
- PlanID or a precisely defined Plan class;
- applicable policy/domain;
- approval decision;
- validity/freshness context;
- optional constraints.

A changed PlanID invalidates a Plan-specific approval unless the approval explicitly and safely covers the changed Plan under its declared scope.

## 2.10 Authorization request

Canonical authorization input conceptually contains:

```text
AuthorizationRequest {
  plan_id
  policy_binding
  decision_certificate
  authenticated_principal
  capability_artifacts[]
  approvals[]
  runtime_domain
  replay_context
  authority_time_context?
}
```

This object is distinct from PlanIR and from DFPL evidence.

## 2.11 Detailed authorization result

The canonical authorization algebra preserves detail:

```text
AuthorizationResult =
    Authorized(AuthorizationArtifact)
  | NotAuthorized(reason)
  | ApprovalRequired(requirements)
  | InvalidAuthorization(error)
```

A coarse API may map these to the earlier three classes, but MUST NOT erase canonical diagnostic information when producing the authoritative result.

## 2.12 Authorization validation order

N-0 candidate validation order:

1. authorization request/artifact canonicality;
2. exact PlanID binding;
3. exact policy/DecisionCertificate binding;
4. DecisionCertificate validity under its verification profile;
5. authenticated-principal validity;
6. capability canonicality/authentication;
7. delegation-chain validation;
8. validity/freshness and required revocation checks;
9. operation-by-operation capability coverage;
10. approval requirements;
11. replay/one-shot constraints;
12. emit AuthorizationResult.

This order is operational authorization logic, not DFPL Law evaluation precedence.

## 2.13 Semantic-verdict binding

The authorization policy states which semantic verdict(s) permit consideration for authorization.

For ordinary privileged execution, a policy SHOULD require semantic `Permit`/`Accept` from the exact DecisionCertificate bound to the Plan candidate transition.

`Deny`, `PreconditionFailure`, `PostconditionFailure`, or `Invalid` cannot be converted to `Authorized` merely by possessing a capability unless an explicitly separate recovery/admin policy defines a distinct Plan and Law path.

## 2.14 Revocation

Revocation semantics are profile-dependent because checking revocation may require external state.

A capability profile MUST declare whether it is:

- non-revocable until expiry;
- revocable with online/live check;
- revocable against a supplied signed snapshot/epoch;
- revocable by another explicitly defined mechanism.

A runtime operating offline MUST NOT claim live revocation freshness it did not verify.

## 2.15 Freshness and authority time

Time is explicit authorization context, not an implicit DFPL-K clock.

If validity windows or approval expiry are enforced, the authorization request supplies a profile-defined trusted/attested time context or equivalent freshness epoch.

The security claim must match the time source actually checked.

## 2.16 Replay and use constraints

Authorization artifacts bind to replay policy:

- one-shot;
- bounded-use;
- reusable under explicit conditions.

One-shot authorization MUST be consumed/recorded atomically enough for the applicable runtime profile to prevent straightforward replay.

A reusable authorization MUST define what changes to state/context still preserve validity.

## 2.17 AuthorizationArtifact

On success, emit an artifact conceptually containing:

```text
AuthorizationArtifact {
  authorization_id
  plan_id
  decision_certificate_id_or_commitment
  principal_id
  capability_ids[]
  approval_ids[]
  domain
  replay_policy
  validity_context
  authorization_profile
}
```

`AuthorizationID` is content-bound under explicit domain separation and excludes its own field from the hashed body.

The Effect Gateway executes only against a valid artifact whose PlanID equals the execution PlanID.

## 2.18 Capability does not mutate Law meaning

Capability possession is runtime authority. It does not modify the DFPL semantic result.

If a Law needs to reason about role/authority facts, verified facts must be supplied through its explicit evidence schema. This is distinct from the gateway deciding whether the runtime may act.

## 2.19 Failure reasons

Initial `NotAuthorized`/invalid reasons include:

```text
SemanticVerdictNotPermitting
PlanBindingMismatch
DecisionCertificateInvalid
AuthenticationInvalid
CapabilityMissing
CapabilityInvalid
CapabilityExpired
CapabilityRevokedOrUnverified
DelegationInvalid
ScopeViolation
ConstraintViolation
ApprovalMissing
ApprovalInvalid
ReplayDetected
FreshnessInsufficient
DomainMismatch
AuthorizationMalformed
```

Exact detailed algebra may be refined without collapsing categories into semantic DFPL verdicts.

## 2.20 Theorem/property targets

- **T-AUTH-01 Plan binding:** Authorized artifacts bind to exactly one PlanID (or explicitly defined safe Plan class for a delegated profile).
- **T-AUTH-02 Policy binding:** ordinary authorization binds to the exact DecisionCertificate/policy evaluated.
- **T-AUTH-03 No authority amplification:** valid delegation cannot create rights/scope/validity broader than the parent chain.
- **T-AUTH-04 Coverage:** Authorized implies every privileged Plan operation is covered by effective capability authority.
- **T-AUTH-05 Principal binding:** capabilities requiring a subject are usable only by the authenticated subject or an explicitly valid representation/delegation relation.
- **T-AUTH-06 Revocation honesty:** a profile never claims revocation freshness stronger than the evidence/check actually performed.
- **T-AUTH-07 Replay compliance:** one-shot/bounded-use artifacts cannot be accepted outside their declared use policy under the runtime model.
- **T-AUTH-08 Semantic separation:** authorization processing does not mutate the DFPL semantic verdict.
- **T-AUTH-09 TOCTOU binding:** Effect Gateway acceptance implies execution PlanID equals authorized PlanID.

These are obligations, not yet mechanically proved.

## 2.21 Freeze consequence

PRIMA now has an explicit authority model between semantic verification and effects: authenticated principals, attenuating capabilities, approvals, replay/freshness policy, detailed authorization results, and an authorization artifact bound to the exact Plan and Decision Certificate.

**NEXT PRIMA:** §3 Effect Gateway and Outcome Semantics, including operation execution contracts, idempotency, failure/compensation behavior, receipt production, divergence detection, and runtime correspondence.
