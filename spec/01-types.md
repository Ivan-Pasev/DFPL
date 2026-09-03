# Ω-DFPL §1 — Canonical Value Domain and Type System

**Status:** normative draft / freeze candidate

Minimum Core value/type families:

- `Bool`
- `Int`
- `Bytes`
- `Text`
- `Digest<A,N>`
- `Address<D>`
- `Option<T>`
- `List<T>`
- `Set<K>`
- `Map<K,V>`
- structural `Record`

## Core rules

- `Int` has exact mathematical integer semantics.
- IEEE-754 `Float` is excluded from minimum Core semantics.
- `Text` uses a Kernel-pinned Unicode version and normalization policy.
- `Bytes`, `Text`, `Digest` and `Address` are distinct types.
- `Digest` includes algorithm identity; `Address` includes address-domain identity.
- no universal untyped null: use `Option<T>`.
- no implicit coercions.
- Set/Map canonicalization is independent of host insertion order.
- concrete canonical values are finite, well-founded structures.
- target resource/range limits must reject unsupported values rather than truncate/wrap/weaken semantics.

Exact Rational and `Decimal<S>` are standard profile candidates; complex, ordinal, modular, symbolic and quantum systems remain explicit profiles/research until fully specified.
