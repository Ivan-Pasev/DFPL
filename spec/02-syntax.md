# Ω-DFPL §2 — DFPL-S0 Canonical Surface Syntax

**Status:** normative draft / freeze candidate

DFPL-S0 is a typed, pure, finite S-expression transition-policy language.

Compilation path:

`DFPL-S0 -> Parse -> AST -> Resolve -> Typed AST -> Normalize -> Canonical Law IR`

## Top-level forms

- `module`
- `type`
- `const`
- `law`
- `context`

Law clauses:

- `requires`
- `forbids`
- `ensures`
- `invariant-pre`
- `invariant-post`
- `invariant-transition`

Explicit phase references:

- `(pre ...)`
- `(post ...)`
- `(evidence ...)`

## Minimum-kernel exclusions

No runtime `eval`, mutation, IO, network access, hidden time/randomness, arbitrary recursion, dynamic field lookup, or agent spawning.

Macros/functions/recursion may exist in PRIMA/DFPL-X, but must lower into finite Core/Plan objects before the applicable verification/authorization boundary.

S-expression syntax is chosen for explicit tree structure and deterministic parsing; DFPL does not inherit Scheme/Common Lisp semantics automatically.
