# Ω-DFPL §6 — Dynamic Semantics

**Status:** normative draft / freeze candidate

## 6.0 Purpose

Dynamic semantics defines the exact meaning of evaluating a well-formed Canonical `LawIRBody` against explicit pre-state, candidate post-state, and evidence.

```text
EvalLaw_K(LawIRBody, pre, post, evidence) -> Verdict
```

The evaluator is pure, deterministic, effect-free, and Kernel-relative.

## 6.1 Evaluation context

```text
EvalContext {
  pre_state
  post_state
  evidence
  locals
}
```

All decision-relevant information is present in the context. Wall-clock time, randomness, filesystem state, network state, environment variables, mutable globals, host process state, and external tools are inaccessible unless already represented explicitly as typed state/evidence.

## 6.2 Expression judgment

Primary judgment:

```text
K ; Γ ⊢ e ⇓ v
K ; Γ ⊢ e ⇑ err
```

For a well-typed canonical expression, evaluation returns exactly one canonical value or exactly one evaluation error.

## 6.3 Reference lookup

`Ref(PRE,path,T)` reads only `pre_state`.

`Ref(POST,path,T)` reads only `post_state`.

`Ref(EVIDENCE,path,T)` reads only `evidence`.

`LocalRef(depth,slot,T)` resolves only against the canonical lexical environment.

Missing or structurally invalid fields yield explicit evaluation errors; there is no dynamic fallback or string-based lookup.

## 6.4 Literal and constructor evaluation

Canonical literals evaluate to themselves.

Option/List/Set/Map/Record/Digest/Address constructors evaluate their children recursively and produce values only if all children evaluate successfully and constructor-specific canonical constraints remain satisfied.

A runtime must not silently repair malformed canonical values during evaluation.

## 6.5 Integer arithmetic

Core integer operations use mathematical `Int` semantics:

```text
Add(a,b)
Sub(a,b)
Neg(a)
Mul(a,b)
```

No abstract overflow exists in DFPL semantics. A bounded target that cannot represent an input/result must reject it under its support profile rather than wrap or saturate.

`quot` and `rem` remain outside N-0 until their sign/division rules are separately frozen.

## 6.6 Equality and ordering

`Eq`/`Ne` operate only on values whose normalized type supports canonical equality.

Minimum-Core ordering operators `Lt/Le/Gt/Ge` apply only to `Int`.

No locale-dependent Text ordering is used for Law evaluation unless introduced by a future explicit profile.

## 6.7 Boolean semantics

`Not(x)` evaluates `x`; non-Bool cannot occur after static checking except through malformed IR, which is invalid before semantic evaluation.

`And(a,b)` is left-to-right short-circuiting:

- if `a ⇓ false`, result is `false` and `b` is not evaluated;
- if `a ⇓ true`, evaluate `b`;
- if `a ⇑ err`, propagate `err`.

`Or(a,b)` is left-to-right short-circuiting:

- if `a ⇓ true`, result is `true` and `b` is not evaluated;
- if `a ⇓ false`, evaluate `b`;
- if `a ⇑ err`, propagate `err`.

Short-circuit behavior is normative because it affects which evaluation error may be observed.

## 6.8 Conditional semantics

`If(c,t,f)` evaluates `c` first.

- `c ⇓ true` => evaluate only `t`;
- `c ⇓ false` => evaluate only `f`;
- `c ⇑ err` => propagate `err`.

The non-selected branch is not evaluated.

## 6.9 Let semantics

N-0 `let` bindings are simultaneous.

Each binding expression is evaluated in the outer lexical environment, in canonical slot order. If all succeed, the resulting values form one immutable lexical frame and the body evaluates under that extended frame.

If binding `i` fails, evaluation stops with that error; later bindings are not evaluated.

## 6.10 Expression errors

Initial `EvalError` algebra:

```text
MissingField
InvalidReference
InvalidLocalReference
MalformedCanonicalValue
UnsupportedOperator
DigestConstructionError
AddressConstructionError
ResourceLimitExceeded(profile)
InternalInvariantViolation
```

Type mismatches should have been rejected before Canonical IR admission. If encountered due to malformed IR, the evaluator returns `InternalInvariantViolation` or the profile-defined equivalent and MUST NOT coerce values.

## 6.11 Clause evaluation

Each canonical clause contains `clause_id` and `Expr<Bool>`.

Clause evaluation yields:

```text
ClausePass(clause_id)
ClauseFail(clause_id)
ClauseEvalError(clause_id, err)
```

For `forbids`, Boolean interpretation is inverted at the Law phase boundary: predicate `true` means the prohibition is activated.

## 6.12 Normative phase order

N-0 Law evaluation uses deterministic first-failure phase order:

1. validate input state/evidence values against canonical context schemas;
2. pre-state invariants;
3. prohibitions;
4. requirements;
5. postconditions;
6. post-state invariants;
7. transition invariants;
8. `Accept`.

Within each phase, clauses are visited in their canonical ClauseID order from §4/§5.

No cross-phase severity lattice is used.

## 6.13 First-failure rule

The first failing/erroring clause in normative phase/order determines the detailed Verdict.

Later clauses/phases are not evaluated.

This makes diagnostics and evaluation cost deterministic and avoids unspecified aggregation behavior.

A future explicit diagnostic profile MAY evaluate additional clauses for reporting, but such diagnostics MUST NOT alter the canonical semantic Verdict produced by N-0.

## 6.14 Detailed Verdict algebra

```text
Verdict =
    Accept
  | EvidenceError(error)
  | PreInvariantViolation(clause_id)
  | Forbidden(clause_id)
  | RequirementRejected(clause_id)
  | PostconditionViolation(clause_id)
  | PostInvariantViolation(clause_id)
  | TransitionInvariantViolation(clause_id)
  | EvalError(clause_id, error)
  | Invalid(error)
```

`Invalid` represents failure to admit/evaluate a supposedly canonical semantic input object, not a policy denial.

`EvidenceError` is used when evidence/context construction or schema validation fails before clause evaluation under the active evidence profile.

## 6.15 Coarse VerdictClass mapping

```text
Accept                            -> Permit
Forbidden                         -> Deny
PreInvariantViolation             -> PreconditionFailure
RequirementRejected               -> PreconditionFailure
PostconditionViolation            -> PostconditionFailure
PostInvariantViolation            -> PostconditionFailure
TransitionInvariantViolation      -> PostconditionFailure
EvidenceError                     -> Invalid
EvalError                          -> Invalid
Invalid                            -> Invalid
```

This mapping is normative for N-0 APIs unless a future Kernel version explicitly changes it.

Detailed Verdict remains authoritative; `VerdictClass` is a projection.

## 6.16 Input schema validation

Before clauses execute, `pre_state`, `post_state`, and `evidence` must match the exact normalized schemas embedded in `LawIRBody`.

Failure produces `EvidenceError` for evidence-profile failures or `Invalid` for malformed/mismatched canonical state objects according to the exact source of failure.

No missing field defaults are inferred unless represented by `Option<T>` in the schema.

## 6.17 Preconditions and prohibitions

Pre-invariant predicate `false` -> `PreInvariantViolation`.

Prohibition predicate `true` -> `Forbidden`.

Requirement predicate `false` -> `RequirementRejected`.

Evaluation errors in any of these predicates -> `EvalError(clause_id, err)`.

## 6.18 Postconditions and invariants

Postcondition predicate `false` -> `PostconditionViolation`.

Post-invariant predicate `false` -> `PostInvariantViolation`.

Transition-invariant predicate `false` -> `TransitionInvariantViolation`.

These verdicts describe the supplied candidate transition; the evaluator does not mutate state or attempt repair.

## 6.19 Determinism

For a fixed Kernel and equal canonical inputs:

```text
EvalLaw_K(L, pre, post, evidence) = v1
EvalLaw_K(L, pre, post, evidence) = v2
--------------------------------------------
v1 = v2
```

Determinism relies on the previously frozen properties of canonical values, Canonical Law IR, normalization, clause ordering, exact integer semantics, and explicit input state.

## 6.20 Termination

N-0 evaluation terminates for well-formed finite inputs because:

- Canonical IR is finite;
- there is no recursion or looping in the semantic kernel;
- expression evaluation traverses finite trees;
- collections are finite;
- clause lists are finite;
- `let` introduces finite immutable frames.

Profiles imposing resource limits may terminate earlier with explicit resource failure.

## 6.21 Purity

Evaluation has no external effects. Even operators named `Digest` or `Address` are pure canonical constructors/validators under the Kernel/profile; they do not contact external networks or key stores.

Any external verification required to construct trusted evidence occurs outside this evaluator or in an explicitly declared evidence-verification profile whose result is supplied as semantic input.

## 6.22 Multi-Law aggregation boundary

N-0 §6 defines evaluation of one `LawIRBody` only.

A Scroll/LawSet profile that combines multiple Laws MUST define its own deterministic aggregation rule. No implicit "worst" or minimum ordering across Laws is part of N-0.

## 6.23 Theorem/property targets

- **T-DYN-01 Expression determinism**.
- **T-DYN-02 Expression termination**.
- **T-DYN-03 Short-circuit determinism**.
- **T-DYN-04 Clause determinism**.
- **T-DYN-05 Law determinism**.
- **T-DYN-06 Law termination**.
- **T-DYN-07 First-failure uniqueness**.
- **T-DYN-08 Accept soundness relative to evaluated clauses**: `Accept` implies every clause evaluated under N-0 returned its required truth value.
- **T-DYN-09 Phase safety preservation**: runtime lookup never observes a phase forbidden by the canonical reference.
- **T-DYN-10 No-effect theorem**: semantic evaluation cannot produce an external effect.
- **T-DYN-11 VerdictClass totality**: every detailed Verdict maps to exactly one coarse class.

These are proof obligations, not yet mechanically proved.

## 6.24 Freeze consequence

DFPL-K now has a complete candidate path from source through typing, normalization, Canonical Law IR, and deterministic evaluation to a detailed Verdict.

**NEXT:** §7 Detailed Decision Algebra and Decision Semantics, including canonical diagnostic payloads, verdict identity/serialization requirements, optional LawSet aggregation profiles, and formal relationships used by Decision Certificates.
