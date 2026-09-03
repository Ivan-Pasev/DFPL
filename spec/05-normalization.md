# Ω-DFPL §5 — Normalization

**Status:** normative draft / freeze candidate

## 5.0 Purpose

Normalization maps a well-formed typed DFPL-S0 module/Law into one Canonical Law IR representation without inventing semantic meaning.

`Normalize_K : TypedLaw -> Result<LawIRBody, NormalizationError>`

Normalization runs only after §3 static closure. It is deterministic, effect-free, finite, and Kernel-relative.

## 5.1 Core obligations

For every well-formed accepted Law `L`:

- normalization terminates;
- one input has one normalized output;
- the result is well-formed Canonical Law IR;
- declared non-semantic source variation disappears;
- semantic distinctions are preserved;
- applying normalization to an already normalized object is idempotent in the corresponding IR-normalization relation.

Target properties:

`N(L) = IR`

`N_IR(IR) = IR`

and therefore conceptually `N(N(L)) = N(L)` across the typed-source/IR boundary.

## 5.2 Normalization pipeline

N-0 normalizes in this order:

1. validate the typed/source object is §3 well-formed;
2. normalize all type descriptors;
3. normalize identifier text according to the Kernel-pinned Unicode policy;
4. evaluate/replace closed constants under the compile-time constant evaluator;
5. erase type aliases;
6. convert phase-qualified paths to resolved structural references;
7. alpha-normalize local binders;
8. normalize values and collection constructors;
9. normalize expression trees;
10. normalize ClauseIDs and detect post-normalization collisions;
11. partition clauses by canonical class;
12. sort clauses within each class by canonical ClauseID order;
13. normalize context schemas;
14. construct `LawIRBody`;
15. validate `KernelID |- LawIRBody wf`.

A failed step returns a normalization error and no Canonical Law IR artifact.

## 5.3 Type normalization

All aliases are recursively replaced by normalized structural type descriptors.

Examples:

`type Amount = Int` normalizes every semantic use of `Amount` to `Int`.

Structural Record fields are ordered by canonical normalized field identifier order. Parameterized types recursively normalize their parameters.

Type normalization is acyclic because §3 rejects cyclic aliases.

## 5.4 Text and identifier normalization

Text values and identifiers use the Unicode version/normalization policy pinned by the Kernel Descriptor.

Normalization MUST NOT perform locale-sensitive case folding, transliteration, homoglyph replacement, or semantic-language equivalence.

If two distinct source identifiers/ClauseIDs normalize to the same canonical identifier in one namespace/Law, normalization fails with a collision error rather than silently merging them.

## 5.5 Constant normalization

A source constant is replaced by its canonical value before LawIRBody construction.

`EvalConst_K(e) -> v`

is defined only for closed, pure compile-time expressions whose operators already have frozen exact compile-time semantics in the active Kernel.

A constant expression containing a reserved-but-not-semantically-frozen operator is rejected rather than guessed from a host language.

Constants do not survive into N-0 LawIRBody as source-level names.

## 5.6 Reference normalization

A statically resolved source reference becomes a canonical structural reference:

```text
Ref {
  phase
  path: [FieldId...]
  type
}
```

`FieldId` is the normalized structural field identity assigned by the canonical schema representation, not a runtime string lookup.

Reference normalization preserves the §3 resolved phase and type; it performs no new lookup against external state.

## 5.7 Alpha-invariant local binding representation

Local source names are non-semantic. N-0 therefore normalizes `let` binders to positional lexical slots.

A canonical representation uses lexical depth plus slot within the simultaneous binding group:

`LocalRef { depth, slot, type }`

Binding groups preserve source expression order only where that order is semantically required by the canonical `let` representation; binder *names* are erased.

Thus harmless renaming:

`(let ((x 1)) (+ x 1))`

and

`(let ((y 1)) (+ y 1))`

produce identical Canonical IR.

Because N-0 forbids shadowing, slot assignment is deterministic and simple; the representation remains compatible with future nested scopes.

## 5.8 Expression normalization

Normalization is structural, not an unrestricted optimizer.

It MUST:

- normalize all child expressions;
- replace constants with canonical values;
- replace state/evidence paths with canonical `Ref` objects;
- replace local names with `LocalRef` slots;
- erase static `as` annotations after successful type checking when they add no semantic information;
- normalize constructor type descriptors and values;
- normalize collection/record ordering where semantically unordered.

It MUST NOT perform algebraic rewrites such as commutativity-based reordering, Boolean theorem proving, dead-code elimination, or arbitrary constant folding unless a future Kernel explicitly defines those rewrites as canonical semantics.

This prevents optimizer sophistication from changing Law identity.

## 5.9 Canonical structural order

§5 defines a Kernel-level total structural order `CanonicalOrder_K` over normalized identifiers, types, values, fields, and clause identifiers sufficient for deterministic ordering.

This order is semantic-structure-level and MUST NOT depend on host map iteration or a not-yet-frozen serialization library.

§8 canonical byte encoding SHALL encode objects consistently with this already-defined structural order.

For Text/identifiers, order is lexicographic over normalized Unicode scalar values.
For integer values, order is mathematical integer order when value ordering is needed.
For tagged compound objects, compare normalized type/tag first and recursively compare canonical components.

The exact tag registry is frozen with the Kernel Descriptor/encoding specification.

## 5.10 Collections

### List

Element order is semantic and preserved after recursively normalizing elements.

### Set

Elements are recursively normalized, checked for equality/duplicates after normalization, and sorted by `CanonicalOrder_K`.

Two distinct source elements that normalize to the same canonical value produce `DuplicateNormalizedSetElement` rather than silent deduplication.

### Map

Keys and values normalize recursively. Duplicate canonical keys after normalization are an error. Entries are sorted by canonical key order.

### Record

Fields normalize recursively, collisions after identifier normalization are errors, and fields are sorted by canonical field identifier order.

## 5.11 Clause normalization

Every ClauseID is Unicode-normalized and retained as content/diagnostic identity.

If two source ClauseIDs normalize to the same canonical ClauseID, normalization fails.

Clauses are partitioned into the six §4 structural classes. Within a class, order is ascending canonical ClauseID order.

The class serialization/identity order remains:

1. pre-state invariants;
2. prohibitions;
3. requirements;
4. postconditions;
5. post-state invariants;
6. transition invariants.

This does not define dynamic evaluation precedence.

## 5.12 Context/schema normalization

Pre-state, candidate post-state, and evidence schemas are normalized structural Record schemas (or future canonical content-addressed schema references explicitly defined by a Kernel version).

N-0 chooses embedded normalized schema descriptors inside `LawIRBody` to avoid introducing a second unresolved identity dependency before §8.

A future Kernel MAY introduce schema IDs with explicit migration rules.

## 5.13 Source material erased

The following do not survive into `LawIRBody`:

- comments;
- whitespace/layout;
- module/source file path;
- type alias names;
- constant names;
- lexical binder names;
- import/package resolution syntax;
- macro syntax;
- source locations;
- author/provenance metadata;
- target/backend annotations not explicitly semantic in the Kernel.

Source maps MAY be emitted as a separate diagnostic/provenance artifact but are excluded from Law semantic identity.

## 5.14 Normalization errors

Initial error algebra includes:

```text
InputNotWellFormed
NormalizedIdentifierCollision
DuplicateNormalizedClauseID
DuplicateNormalizedField
DuplicateNormalizedSetElement
DuplicateNormalizedMapKey
UnsupportedConstOperator
ConstEvaluationError
NonCanonicalText
UnsupportedKernelConstruct
NormalizationInvariantViolation
```

Normalization errors do not produce a semantic Deny or runtime Invalid verdict because no valid Canonical Law IR was produced.

## 5.15 No host-dependent normalization

A conformant normalizer MUST NOT depend on:

- host hash-map iteration order;
- process/object addresses;
- locale;
- platform Unicode defaults;
- host numeric overflow/rounding;
- nondeterministic concurrency;
- filesystem/network state;
- compiler optimization heuristics.

## 5.16 Theorem/property targets

- **T-NORM-01 Determinism:** equal typed input under the same Kernel produces equal LawIRBody or the same normalization error class.
- **T-NORM-02 Termination:** normalization terminates for every §3 well-formed finite input.
- **T-NORM-03 Idempotence:** Canonical Law IR normalization is a fixed point.
- **T-NORM-04 Alpha invariance:** lexical binder renaming does not alter normalized IR.
- **T-NORM-05 Alias erasure:** semantically equivalent type aliases normalize to the same type structure.
- **T-NORM-06 Source-order independence:** declaration/clause/field/map/set source order declared non-semantic does not alter normalized IR.
- **T-NORM-07 Type preservation:** normalized expressions retain their §3 normalized type.
- **T-NORM-08 Phase preservation:** normalized references preserve phase correctness.
- **T-NORM-09 Metadata non-interference:** excluded source/provenance metadata does not alter normalized LawIRBody.
- **T-NORM-10 Well-formed result:** successful normalization yields `KernelID |- LawIRBody wf`.

These are proof obligations, not yet mechanically proved.

## 5.17 Freeze consequence

With §5, DFPL has a deterministic route from fully checked source to a unique target-independent canonical semantic structure.

The next kernel milestone is **§6 Dynamic Semantics**, which will define exact evaluation order, expression evaluation, runtime error propagation, detailed Verdict constructors, and the relationship between clause evaluation and coarse VerdictClass.
