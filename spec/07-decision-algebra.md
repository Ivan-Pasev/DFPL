# Ω-DFPL §7 — Detailed Decision Algebra

**Status:** normative draft / freeze candidate

## 7.0 Purpose

§7 freezes the semantic result domain produced by §6 and the exact relationships between detailed Verdicts, coarse VerdictClass values, diagnostics, LawSet aggregation boundaries, and later Decision Certificates.

The authoritative semantic result is the detailed `Verdict`.

```text
EvalLaw_K(LawIRBody, pre, post, evidence) -> Verdict
ProjectClass_K(Verdict) -> VerdictClass
```

`VerdictClass` is a lossy projection. It MUST NOT replace the detailed Verdict in canonical audit/certificate artifacts.

## 7.1 Verdict algebra

N-0 freezes:

```text
Verdict =
    Accept
  | EvidenceError(EvidenceFailure)
  | PreInvariantViolation(ClauseFailure)
  | Forbidden(ClauseFailure)
  | RequirementRejected(ClauseFailure)
  | PostconditionViolation(ClauseFailure)
  | PostInvariantViolation(ClauseFailure)
  | TransitionInvariantViolation(ClauseFailure)
  | EvalError(EvaluationFailure)
  | Invalid(InvalidFailure)
```

The constructors are disjoint. A conformant evaluator never returns two Verdicts for one canonical evaluation.

## 7.2 ClauseFailure

Clause-based policy failures carry canonical clause identity without embedding prose diagnostics into semantic identity.

```text
ClauseFailure {
  clause_id
  phase
}
```

`phase` is redundant with the Verdict constructor in N-0 but is retained as a typed consistency field for certificate/audit validation. A malformed constructor/phase combination is invalid.

Human-readable messages, source spans, localized text, remediation hints, stack traces, and UI formatting are non-semantic diagnostic metadata and MUST NOT affect Verdict identity.

## 7.3 EvaluationFailure

```text
EvaluationFailure {
  clause_id
  phase
  error
}
```

where `error` is one §6 `EvalError` constructor.

The failure identifies the exact clause whose predicate could not be evaluated under the canonical first-failure order.

Evaluation failure is not policy denial:

```text
EvalError(...) -> VerdictClass.Invalid
```

## 7.4 EvidenceFailure

Evidence/context admission can fail before clause evaluation.

Initial canonical classes:

```text
EvidenceFailure =
    MissingRequiredEvidence(path)
  | EvidenceTypeMismatch(path, expected_type)
  | EvidenceSchemaMismatch(detail_code)
  | EvidenceVerificationFailed(profile, detail_code)
  | EvidenceProfileUnsupported(profile)
```

Where a verifier produces rich external/provenance detail, the canonical Verdict carries only the Kernel/profile-defined semantic failure code and required canonical identifiers. Large external logs remain referenced diagnostic evidence, not embedded semantic prose.

## 7.5 InvalidFailure

`Invalid` represents inability to admit/evaluate the canonical semantic input object independently of a Law predicate.

Initial classes:

```text
InvalidFailure =
    PreStateSchemaMismatch(detail_code)
  | PostStateSchemaMismatch(detail_code)
  | MalformedLawIR(detail_code)
  | UnsupportedKernelConstruct(detail_code)
  | InternalInvariantViolation(detail_code)
```

`Invalid` MUST NOT be re-labeled `Deny` merely to implement fail-closed effects. Runtime fail-closed behavior belongs to authorization/effect policy.

## 7.6 VerdictClass

N-0 coarse domain:

```text
VerdictClass =
    Permit
  | Deny
  | PreconditionFailure
  | PostconditionFailure
  | Invalid
```

Normative projection:

```text
Accept                       -> Permit
Forbidden                    -> Deny
PreInvariantViolation        -> PreconditionFailure
RequirementRejected          -> PreconditionFailure
PostconditionViolation       -> PostconditionFailure
PostInvariantViolation       -> PostconditionFailure
TransitionInvariantViolation -> PostconditionFailure
EvidenceError                -> Invalid
EvalError                    -> Invalid
Invalid                      -> Invalid
```

The projection is total and deterministic.

## 7.7 Why `Forbidden` maps to `Deny`

`Forbidden` is the explicit negative-policy constructor: the Law evaluated a prohibition predicate to true. It is therefore the canonical source of coarse `Deny` in N-0.

A failed `requires` clause is not collapsed into `Deny` because it carries different semantics: a required enabling condition was absent. The distinction is preserved even if an external gateway blocks both outcomes.

## 7.8 Why invariant failures remain pre/post failures

Pre-state invariant failure means the supplied pre-state is outside the Law's admissible starting region.

Post-state and transition invariant failures mean the proposed transition does not establish/retain the required admissible resulting relation.

Therefore N-0 classifies them with the corresponding pre/post failure families rather than generic `Deny`.

## 7.9 Canonical first-failure identity

The detailed Verdict is determined by §6 normative phase order plus canonical ClauseID order.

If multiple predicates would fail, only the first canonical failure contributes to the semantic Verdict.

A diagnostic implementation MAY evaluate additional clauses under a declared non-semantic diagnostic profile, but:

```text
DiagnosticFailures != CanonicalVerdict
```

and additional diagnostics MUST NOT alter DecisionCertificate semantic fields.

## 7.10 Semantic result versus diagnostic envelope

Define a non-normative/auxiliary diagnostic object:

```text
DecisionDiagnostics {
  verdict
  source_locations[]
  human_messages[]
  remediation_hints[]
  trace?
  additional_failures[]?
}
```

Only `verdict` is semantic under N-0 unless a later profile explicitly promotes another field.

This permits rich developer UX without making localized prose or debug traces part of Law semantics.

## 7.11 Verdict identity

Verdict identity is structural, Kernel-relative, and value-based.

Conceptually:

```text
VerdictIdentity = CanonicalVerdictValue(KernelID, Verdict)
```

N-0 does not define a standalone `VerdictID` hash because §9 Decision Certificates will bind the Verdict together with KernelID, LawID, state/evidence commitments, and evaluation profile. If a future Kernel introduces standalone Verdict IDs, it MUST define canonical encoding/domain separation explicitly.

## 7.12 No severity lattice

N-0 defines no global ordering such as:

```text
Invalid > Deny > PostconditionFailure > ...
```

and no arithmetic/minimum aggregation over Verdicts.

The semantic ordering mechanism is solely §6 deterministic phase/ClauseID first failure.

This avoids accidentally treating incomparable semantic categories as a total severity order.

## 7.13 LawSet boundary

N-0 Core evaluates one Law at a time.

A `LawSet` / Scroll aggregation profile MUST explicitly define:

```text
AggregateProfile {
  law_order
  evaluation_strategy
  short_circuit_rule
  aggregate_result_algebra
  diagnostic_rule
}
```

No implicit `worst Verdict`, `minimum`, majority vote, priority vote, or conjunction/disjunction across Laws exists in Core N-0.

## 7.14 Standard LawSet profile candidates

The following are reserved as profile design candidates, not Core semantics:

### AllMustAccept
Evaluate Laws in canonical profile order; first non-`Accept` becomes aggregate result.

### AnyMayAccept
Requires a separately defined result algebra because `Invalid`/failure handling cannot be guessed from Boolean OR.

### PriorityOrdered
Explicit profile-defined Law priority order; first decisive result semantics must be fully defined.

### DiagnosticAll
Evaluate all Laws for diagnostics while retaining a separately specified canonical aggregate result.

None is active merely by being named here.

## 7.15 Decision trace boundary

A semantic implementation MAY generate a deterministic trace:

```text
DecisionTrace {
  phase_entries[]
  clause_visits[]
  expression_events[]?
  terminal_verdict
}
```

But trace granularity is not N-0 semantic identity unless a future trace profile freezes it.

A missing trace cannot invalidate an otherwise conformant semantic Verdict unless a declared profile requires the trace as evidence/certificate payload.

## 7.16 Stability under diagnostic changes

Changing:

- wording,
- localization,
- source location formatting,
- stack-trace formatting,
- remediation text,
- logging verbosity,
- optional diagnostic-all behavior

MUST NOT change the canonical Verdict for identical Kernel/Law/input values.

## 7.17 Decision Certificate interface

§7 freezes the semantic fields later consumed by §9:

```text
DecisionSemanticResult {
  kernel_id
  law_id
  verdict
  verdict_class
}
```

with invariant:

```text
verdict_class == ProjectClass_K(verdict)
```

§9 will additionally bind pre/post/evidence commitments, evaluation profile, optional evaluator/proof/attestation identity, validity context, and certificate identity.

## 7.18 Fail-closed integration rule

External systems MAY define:

```text
MayExecute(v) = true only if ProjectClass(v) == Permit
```

but this integration rule MUST NOT mutate non-Permit Verdicts into `Deny`.

Therefore:

```text
Invalid -> DoNotExecute
```

is valid gateway policy while preserving:

```text
Invalid != Deny
```

## 7.19 Equality

Two canonical Verdict values are equal iff they have the same constructor and equal canonical payload fields under the same Kernel type definitions.

Human diagnostic attachments do not participate.

## 7.20 Compatibility across Kernel versions

Different Kernel versions MAY define compatible Verdict behavior but are not assumed identical merely because constructor names match.

A migration/compatibility profile must state whether Verdict/result mappings are:

- exact,
- acceptance-preserving,
- refinement-preserving,
- diagnostic-only compatible,
- incompatible.

No automatic cross-Kernel comparison is defined.

## 7.21 Formal properties

- **T-DEC-01 Verdict Constructor Disjointness** — one canonical Verdict inhabits exactly one constructor.
- **T-DEC-02 VerdictClass Totality** — every Verdict maps to exactly one VerdictClass.
- **T-DEC-03 VerdictClass Determinism** — equal Verdicts map to equal classes.
- **T-DEC-04 Accept/Permit Exactness** — `ProjectClass(v)=Permit` iff `v=Accept` in N-0.
- **T-DEC-05 Deny Exactness** — `ProjectClass(v)=Deny` iff `v=Forbidden(_)` in N-0.
- **T-DEC-06 Diagnostic Non-Interference** — diagnostic metadata changes cannot change canonical Verdict.
- **T-DEC-07 First-Failure Correspondence** — the Verdict clause payload equals the first failing/erroring clause visited by §6 semantics.
- **T-DEC-08 Certificate Projection Consistency** — a valid later Decision Certificate cannot carry a VerdictClass different from `ProjectClass_K(verdict)`.
- **T-DEC-09 No Implicit LawSet Aggregation** — Core evaluation of one Law is independent of any undeclared multi-Law policy.

These are proof obligations, not yet mechanically proved.

## 7.22 Freeze consequence

DFPL-K now has a fully separated candidate semantic result model: deterministic detailed Verdict, explicit coarse projection, canonical failure payload boundaries, diagnostic non-interference, and a clean interface to Decision Certificates and future LawSet profiles.

**NEXT:** §8 Canonical Encoding and IDs — exact byte-level representation for normalized types/values/LawIR, domain separation, KernelID/LawID construction, length/type tags, Unicode/integer encoding, and test vectors.
