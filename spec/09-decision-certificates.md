# Ω-DFPL §9 — Decision Certificates

**Status:** normative draft / freeze candidate

## 9.0 Purpose

A Decision Certificate is the canonical semantic-result envelope that binds one DFPL evaluation to the exact kernel, law, committed inputs, detailed Verdict, coarse VerdictClass, and verification profile used to establish that result.

A Decision Certificate does **not** itself authorize execution and does not prove more than its declared verification profile establishes.

```text
Law + Inputs + Evidence
        |
        v
      DFPL-K
        |
        v
Detailed Verdict
        |
        v
DecisionCertificate
        |
        v
PRIMA Authorization
```

Normative separation:

```text
DecisionCertificate != AuthorizationArtifact
DecisionCertificate != OutcomeReceipt
Hash != Proof
Attestation != SemanticProof
```

## 9.1 Certificate body and artifact

Identity is separated from the body being identified.

```text
DecisionCertificateBody {
  kernel_id
  law_id

  pre_state_commitment
  candidate_post_state_commitment
  evidence_commitments[]

  verdict
  verdict_class

  evaluation_profile
  verification_material?

  evaluator_identity?
  freshness_context?
  replay_context?

  auxiliary_commitments?
}

DecisionCertificate {
  decision_id
  body
  provenance_refs[]?
  transport_metadata?
}
```

`decision_id`, provenance references, transport metadata, human-readable explanations, and delivery timestamps MUST NOT self-participate in the bytes from which `decision_id` is computed unless an explicitly versioned profile promotes a field into the canonical body.

## 9.2 Canonical identity

N-0 uses the §8 canonical encoding and domain-separated identity pattern:

```text
DecisionID = SHA256(
  "DFPL-DECISION-v1\0" ||
  KernelID ||
  EncodeDecisionCertificateBody(body)
)
```

The body MUST already be canonical and Kernel-compatible before DecisionID construction.

## 9.3 Kernel and Law binding

A certificate MUST identify exactly one `KernelID` and one `LawID` for N-0 single-Law evaluation.

Verification MUST reject a certificate if:

- `law_id` is not valid under `kernel_id`;
- the supplied LawIRBody does not recompute to the stated `law_id`;
- the verifier does not support the stated Kernel;
- the certificate body uses structures inconsistent with that Kernel.

Law-set evaluation is outside N-0 unless an explicit aggregation profile defines the LawSet identity, order and result algebra.

## 9.4 Input commitments

The certificate binds the exact evaluation inputs through typed commitments.

```text
InputCommitment {
  object_kind
  schema_or_type_id
  digest_algorithm
  digest_bytes
}
```

At minimum:

```text
pre_state_commitment
candidate_post_state_commitment
evidence_commitments[]
```

A commitment establishes binding to bytes under the selected hash assumptions; it does not establish that the committed external observation is true.

## 9.5 Commitment construction

Where the input is itself a canonical DFPL object, the default commitment is:

```text
Commit(obj, domain) = SHA256(domain || CanonicalEncode_K(obj))
```

Input families SHOULD use distinct domain separators, for example:

```text
DFPL-PRESTATE-v1\0
DFPL-POSTSTATE-v1\0
DFPL-EVIDENCE-v1\0
```

If a profile commits to an external Merkle root, ledger root, signed document, or other evidence structure instead of raw canonical object bytes, that construction MUST be identified explicitly by the evidence/verification profile.

## 9.6 Evidence commitment list

Evidence commitments are canonically ordered.

N-0 candidate rule:

```text
sort by (evidence_slot_id, commitment_type, digest_bytes)
```

Duplicate `evidence_slot_id` entries are invalid unless the Law schema/profile explicitly allows a collection at that slot.

The order of arrival or host map iteration is not semantic.

## 9.7 Verdict binding

The certificate MUST carry the exact detailed `Verdict` from §7 and the corresponding deterministic `VerdictClass` projection.

Verification MUST check:

```text
project_verdict_class(verdict) == verdict_class
```

A mismatched pair invalidates the certificate.

The certificate MUST NOT replace a detailed Verdict with only a coarse class.

## 9.8 Evaluation profile

`evaluation_profile` identifies how the semantic result was established.

N-0 profile classes:

```text
DirectLocal
DirectRemote
ProofCarrying
Optimistic
Attested
AnchorOnly
```

These classes are labels for profile families, not interchangeable security guarantees. Each concrete profile MUST define its verification algorithm and trust assumptions.

## 9.9 DirectLocal profile

`DirectLocal` means the verifier recomputes the DFPL evaluation locally from the exact canonical Law and inputs under the stated Kernel.

Required condition:

```text
Recompute_K(L, pre, post, evidence) == certificate.verdict
```

This is the reference semantic-verification mode when all canonical inputs are available.

## 9.10 DirectRemote profile

`DirectRemote` means a remote evaluator reports the result and provides authenticated/attested result material defined by the profile.

Remote authenticity alone does not prove semantic correctness.

A DirectRemote profile MUST state whether the verifier:

- trusts the evaluator;
- additionally recomputes;
- checks reproducible execution evidence;
- validates hardware/workload attestation;
- performs quorum comparison;
- or uses another explicit mechanism.

## 9.11 ProofCarrying profile

`ProofCarrying` provides proof material whose verifier is specified independently of the evaluator.

Examples may include a zero-knowledge proof, formal proof certificate, or another mechanically checkable witness.

The profile MUST bind at least:

```text
KernelID
LawID
input commitments
Verdict
proof-system identity/version
verification key or equivalent immutable reference
```

A proof verifies only the statement encoded by its circuit/theorem/profile.

## 9.12 Optimistic profile

An `Optimistic` profile accepts a bonded/asserted result subject to challenge/fraud-proof rules.

The certificate MUST identify the applicable challenge profile/window/context. Until that profile's finality rule is satisfied, consumers MUST NOT silently treat the result as having stronger finality than it has.

## 9.13 Attested profile

An `Attested` profile binds the certificate result to one or more authenticated evaluators/committees/workloads.

The profile MUST define:

- signer/evaluator identity model;
- quorum or threshold, if any;
- key/version policy;
- revocation/freshness handling;
- exact signed bytes;
- trust assumptions.

Attestation says who/what asserted the result. It does not equal proof of semantic correctness unless the trust model explicitly assumes that evaluator is correct.

## 9.14 AnchorOnly profile

`AnchorOnly` binds a Decision Certificate body/DecisionID into another system without independently establishing the semantic evaluation.

Example: storing `DecisionID` on a ledger.

Normative rule:

```text
AnchorOnly => content/time/order evidence as profile-defined
AnchorOnly != semantic proof
```

## 9.15 Verification material

Verification material is profile-specific and MUST be typed/versioned.

Conceptually:

```text
VerificationMaterial {
  profile_id
  material_type
  material_bytes_or_refs
}
```

The certificate body MAY contain commitments/references to large proof/attestation artifacts rather than embedding them, provided the profile defines integrity and retrieval requirements.

## 9.16 Evaluator identity

`evaluator_identity` is optional in semantic Core because DirectLocal evaluation may not require a persistent actor identity.

Where present it MUST be an explicit typed identity/attestation reference. A display name/string is not authentication.

Evaluator identity does not grant runtime authority.

## 9.17 Freshness context

A certificate MAY bind an explicit freshness context, e.g.:

```text
FreshnessContext {
  issued_context?
  not_before?
  not_after?
  observation_epoch?
  trusted_time_source_profile?
}
```

DFPL-K has no hidden wall clock. Freshness verification occurs only through an explicit profile/context supplied to the verifier/authorization layer.

A certificate does not become invalid merely because local wall-clock time changed unless its profile defines that rule.

## 9.18 Replay context

A semantic Decision Certificate is normally reproducible and therefore may be replayed as data.

Whether it may be reused for authorization is a separate PRIMA policy.

The body MAY bind a replay context such as:

```text
ReplayContext {
  nonce?
  workflow_id?
  plan_id?
  authorization_scope_ref?
}
```

Normative separation:

```text
CertificateReplay != AuthorizationReplay
```

One-shot execution semantics belong to capability/authorization/replay state, not to the mathematical determinism of the semantic verdict.

## 9.19 Plan binding profile

For PRIMA use, a certificate SHOULD bind the exact Plan/CandidateTransition context when the policy decision is specific to that Plan.

Candidate extension:

```text
auxiliary_commitments.plan_id = PlanID
```

or a versioned profile-defined field in the canonical body.

The binding MUST be unambiguous before authorization. Authorization MUST NOT accept a certificate evaluated for one candidate transition as authority for a materially different Plan.

## 9.20 Certificate verification algorithm

Conceptual N-0 verification:

1. decode using the declared Kernel/profile;
2. reject noncanonical encoding;
3. recompute and verify `DecisionID`;
4. verify `KernelID` support;
5. verify/recompute `LawID` where Law body is supplied;
6. verify input commitments against supplied inputs/artifacts where applicable;
7. verify `Verdict -> VerdictClass` projection;
8. verify the selected evaluation profile/material;
9. verify freshness/replay context only where the consuming profile requires it;
10. return a typed verification result.

## 9.21 Verification result

Certificate verification is not itself a DFPL policy Verdict.

Candidate result algebra:

```text
CertificateVerificationResult =
    CertificateValid(profile_assurance)
  | UnsupportedKernel
  | UnsupportedProfile
  | NonCanonicalCertificate
  | DecisionIdMismatch
  | LawIdMismatch
  | InputCommitmentMismatch(slot)
  | VerdictClassMismatch
  | VerificationMaterialInvalid(reason)
  | FreshnessInvalid(reason)
  | ReplayContextInvalid(reason)
  | ArtifactUnavailable(ref)
```

A fail-closed integration may refuse authorization for any non-valid result but MUST NOT relabel certificate-verification failures as semantic `Deny`.

## 9.22 Assurance is profile-relative

A certificate consumer MUST interpret assurance from the concrete verification profile, not merely from the fact that a `DecisionID` exists.

Illustratively:

```text
DirectLocal     -> independently recomputed semantic result
ProofCarrying   -> proof statement verified as profile-defined
Attested        -> authenticated assertion under stated trust model
AnchorOnly      -> committed/anchored bytes under stated external guarantees
```

There is no universal total ordering over these assurances unless a higher-level profile explicitly defines one.

## 9.23 Tamper behavior

Any canonical-body mutation MUST change DecisionID subject to hash assumptions.

Tampering with noncanonical transport metadata MAY leave DecisionID unchanged by design.

Consumers MUST know which fields are identity-bound and which are not.

## 9.24 Privacy and selective disclosure

The minimum certificate SHOULD prefer commitments to potentially sensitive pre/post/evidence values rather than embedding all values.

A verification profile may use selective-disclosure or ZK mechanisms, but it MUST define which semantic statement is proven and how commitments correspond to the evaluated inputs.

Privacy mechanisms MUST NOT create hidden decision inputs unavailable to the stated semantic model.

## 9.25 Certificate transport envelope

Transport/storage wrappers may add:

- MIME/content type;
- compression;
- external signatures;
- routing metadata;
- repository/ledger references;
- human-readable explanation.

These wrappers are outside `DecisionCertificateBody` unless explicitly promoted by profile versioning.

## 9.26 Decision Certificate versus OutcomeReceipt

The certificate states the result of policy evaluation over a **candidate** transition.

The OutcomeReceipt records what was observed during/after **effect execution**.

```text
DecisionCertificate(candidate_post) != OutcomeReceipt(observed_post)
```

A later audit may compare their commitments and classify correspondence/divergence.

## 9.27 Decision Certificate versus AuthorizationArtifact

Authorization consumes a verified Decision Certificate plus authority context.

```text
Authorize(
  verified_decision_certificate,
  principal,
  capabilities,
  approvals,
  freshness,
  replay_state
) -> AuthorizationResult
```

A certificate containing `Permit` MUST NOT bypass capability/approval checks.

## 9.28 Canonical certificate bytes

The canonical encoding MUST use §8 structural encoding, fixed field order, typed optional fields, canonical lists/maps, and profile-pinned tags.

No JSON key order, protobuf field-number default, host struct layout, or database row serialization is normative unless an explicit profile proves byte-equivalence to the canonical encoding.

## 9.29 Golden vectors

§9 requires machine-readable vectors for at least:

1. Permit certificate;
2. Forbidden/Deny certificate;
3. precondition failure certificate;
4. postcondition failure certificate;
5. Invalid/evaluation failure certificate;
6. VerdictClass mismatch rejection;
7. altered pre-state commitment rejection;
8. altered LawID rejection;
9. DecisionID tamper rejection;
10. unsupported verification profile;
11. AnchorOnly certificate clearly distinguished from semantic proof;
12. DirectLocal recomputation success/failure.

Golden hashes remain provisional until the exact §8 tag registry/Kernel Descriptor is frozen and independently reproduced.

## 9.30 Security limits

A valid Decision Certificate does not by itself establish:

- truth of raw external observations;
- legal authority;
- runtime capability;
- effect execution;
- effect success;
- observed post-state correspondence;
- universal correctness of an evaluator outside the selected verification profile.

The certificate is an auditable semantic-result binding, not an omnipotent trust token.

## 9.31 Theorem/property targets

- **T-CERT-01 Identity determinism:** equal canonical bodies produce equal DecisionID.
- **T-CERT-02 Body sensitivity:** canonical-body mutation changes bytes and, subject to hash assumptions, DecisionID.
- **T-CERT-03 Verdict projection consistency:** a valid certificate carries the normative §7 VerdictClass projection.
- **T-CERT-04 Input binding:** supplied inputs verify exactly against the committed input bytes/profile.
- **T-CERT-05 Law binding:** supplied Law under Kernel recomputes to the stated LawID.
- **T-CERT-06 DirectLocal correspondence:** valid DirectLocal verification implies recomputed evaluator output equals the certificate Verdict.
- **T-CERT-07 Profile separation:** AnchorOnly/Attested profiles cannot be interpreted as stronger verification classes without explicit profile rules.
- **T-CERT-08 Authorization separation:** certificate validity alone does not imply Authorized.
- **T-CERT-09 Receipt separation:** certificate validity alone does not imply Executed or observed state correspondence.
- **T-CERT-10 Replay separation:** semantic certificate reproducibility does not replenish consumed runtime authority.

These are obligations, not mechanically proved claims.

## 9.32 Freeze consequence

DFPL-K now has a candidate canonical semantic-result object connecting deterministic evaluation to external verification and PRIMA authorization without collapsing trust boundaries.

```text
Canonical Law/Input
 -> DFPL-K
 -> Verdict
 -> DecisionCertificate
 -> Certificate Verification
 -> PRIMA Authorization
```

**NEXT:** §10 Conformance, Security, Versioning, and Migration — define conformance classes, canonical corpus obligations, Kernel compatibility relations, migration semantics, security assumptions, and the release/freeze contract for N-0.