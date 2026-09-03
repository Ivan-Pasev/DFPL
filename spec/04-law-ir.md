# Ω-DFPL §4 — Canonical Law IR

**Status:** normative draft / freeze candidate

## 4.0 Purpose

Canonical Law IR is the semantic convergence object produced after parsing, name resolution, static typing, and source-level expansion/desugaring.

`DFPL-S0 → AST → Resolved AST → Typed AST → Normalize → LawIR`

Law IR MUST contain no unresolved names, aliases, macros, comments, source-layout semantics, imports, dynamic field lookup, or target-specific code.

## 4.1 Identity split

Semantic body and identity envelope are distinct.

```text
LawIRBody {
  context
  pre_invariants[]
  prohibitions[]
  requirements[]
  postconditions[]
  post_invariants[]
  transition_invariants[]
}

LawArtifact {
  kernel_id
  law_id
  body
}
```

`law_id` MUST NOT appear inside the bytes hashed to compute itself.

Candidate identity:

`LawID = H(DS_LAW || KernelID || CanonicalEncode(LawIRBody))`

The exact digest algorithm, domain-separation bytes, and canonical byte encoding remain §8 obligations.

## 4.2 Context

A canonical Law context contains resolved schema descriptors for:

- pre-state,
- candidate post-state,
- evidence.

Schemas MUST be either embedded canonically or referenced through kernel-defined content-addressed schema identities. Human aliases are not semantic identity.

## 4.3 Resolved references

Surface references such as:

`(pre account balance)`

normalize to typed structural references, conceptually:

```text
Ref {
  phase: PRE,
  path: [resolved_field_id...],
  type: Int
}
```

Every reference therefore carries a statically established phase and normalized type.

## 4.4 Canonical expression algebra

Canonical expressions are finite typed trees. Candidate constructors include:

```text
Literal(value)
Const(value)
Ref(phase,path,type)
Let(bindings,body)
If(condition,then,else)
Not(x)
And(a,b)
Or(a,b)
Add(a,b)
Sub(a,b)
Neg(x)
Mul(a,b)
Eq(a,b)
Ne(a,b)
Lt(a,b)
Le(a,b)
Gt(a,b)
Ge(a,b)
Some(x)
None(type)
List(type,values)
Set(type,values)
Map(key_type,value_type,entries)
Record(fields)
Get(record,field_id)
Digest(algorithm,bytes)
Address(domain,bytes)
```

Reserved operators such as integer `quot`/`rem` enter Canonical IR only after their dynamic semantics are frozen.

## 4.5 Clause structure

Each clause carries a unique stable ClauseID and one typed Boolean expression.

```text
Clause {
  clause_id
  predicate: Expr<Bool>
}
```

Clause classes are structurally separated rather than represented by source-order tags.

## 4.6 Canonical clause ordering

Source clause order is not semantic. Within each clause class, canonical order is ascending by canonical ClauseID encoding.

Canonical class order for identity/serialization is:

1. pre-state invariants,
2. prohibitions,
3. requirements,
4. postconditions,
5. post-state invariants,
6. transition invariants.

This ordering is an encoding/identity order. Dynamic evaluation precedence is defined separately in §6 and MUST NOT be inferred solely from serialization order.

## 4.7 Constants and aliases

Constants that can be normalized to closed canonical values are replaced by those values in Law IR.

Type aliases are erased to normalized type descriptors.

Lexical names in `let` bindings are replaced by deterministic binding identities or an equivalent alpha-invariant representation so harmless local renaming does not change semantic identity.

## 4.8 Collection normalization boundary

Law IR represents sets, maps, records, and other semantically unordered structures in canonical structural order. Duplicate set elements, map keys, record fields, or clause IDs are invalid before canonical Law IR is admitted.

## 4.9 Metadata non-interference

The following are outside `LawIRBody` unless deliberately modeled as semantic state/evidence:

- author name,
- timestamps,
- signatures,
- repository URLs,
- comments,
- ScrollDNA,
- package provenance,
- publication metadata.

Therefore changing provenance metadata does not silently change Law semantics.

## 4.10 Law IR well-formedness

Define:

`KernelID ⊢ LawIRBody wf`

iff:

1. every type descriptor is normalized and well-formed;
2. every reference is resolved, typed, and phase-valid;
3. every clause predicate has type Bool;
4. all ClauseIDs are globally unique within the Law;
5. all canonical collection constraints hold;
6. no source-only or extension construct remains;
7. every operator is supported by the declared Kernel;
8. the IR is finite.

Only well-formed Law IR may be canonically encoded or evaluated.

## 4.11 Behavioral equivalence versus content identity

Two Laws may be behaviorally equivalent while having different `LawID`s, for example because ClauseIDs differ.

`BehaviorallyEquivalent(L1,L2)` does not imply `LawID(L1)=LawID(L2)`.

LawID is a content identity over canonical Law IR, not a theorem of extensional equivalence.

## 4.12 Theorem targets

- **IR-01 Construction determinism:** one well-formed typed source object normalizes to one LawIRBody.
- **IR-02 Resolution closure:** Canonical Law IR contains no unresolved identifiers or paths.
- **IR-03 Type preservation:** every canonical expression retains its statically established normalized type.
- **IR-04 Phase preservation:** canonical references preserve §3 phase safety.
- **IR-05 Alpha invariance:** renaming non-semantic lexical binders does not change Canonical Law IR.
- **IR-06 Source-order independence:** reordering semantically unordered source declarations/clauses does not change Canonical Law IR.
- **IR-07 Metadata non-interference:** changes to excluded provenance metadata do not change LawIRBody.

These are proof obligations, not yet claimed mechanically proved.

## 4.13 Freeze consequence

After §4, DFPL obtains a target-independent semantic object suitable for:

- normalization proofs,
- canonical encoding,
- Law identity,
- deterministic evaluation,
- differential conformance,
- formal mechanization.

**NEXT:** §5 Normalization.
