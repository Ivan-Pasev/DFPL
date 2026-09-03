# Ω-DFPL §3 — Static Semantics, Resolution, and Phase Typing

**Status:** normative draft / freeze candidate

Before Canonical Law IR construction a module must be well-formed, resolved, typed, phase-safe, and closed.

Primary judgment:

`Gamma ; Phi |- e : tau`

where `Phi` is the permitted phase set drawn from `{pre, post, evidence}`.

## Static closure rules

- separate namespaces for types/constants/laws/fields/locals;
- type and constant dependency graphs are finite and acyclic;
- declaration order is non-semantic;
- lexical `let` bindings are immutable and simultaneous;
- N-0 forbids lexical shadowing;
- all state/evidence paths resolve statically;
- clause predicates have type `Bool`;
- clause IDs are globally unique within a Law;
- each Law has exactly one explicit context and at least one explicit clause;
- no unresolved extension form may survive.

## Clause phase sets

- pre invariant: `{pre}`
- prohibition: `{pre,evidence}`
- requirement: `{pre,evidence}`
- postcondition: `{pre,post,evidence}`
- transition invariant: `{pre,post}`
- post invariant: `{post}`

Closure invariant:

`WellFormed(M) => NoUnresolvedSemanticChoice(M)`

Theorem targets include name-resolution determinism, type uniqueness, phase safety, resolution completeness, constant normalization termination, and static-checking decidability.
