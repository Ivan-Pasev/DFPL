# DFPL Formalization

The formal program targets the minimum DFPL-K kernel before PRIMA/runtime complexity.

Planned Lean order:

1. Values and normalized types
2. DFPL-S0 syntax / parsed AST model
3. Static environments and phase typing
4. Canonical Law IR
5. Normalization
6. Dynamic evaluation
7. Detailed verdict algebra
8. Canonical identity/encoding definitions
9. Projection/conformance relations

Current theorem obligations include:

- parse determinism;
- name-resolution determinism;
- type uniqueness;
- phase safety;
- static decidability;
- Canonical Law IR construction determinism;
- resolution/type/phase preservation;
- alpha invariance;
- source-order independence where declared non-semantic;
- metadata non-interference;
- normalization termination and idempotence;
- evaluation determinism/termination;
- encoding separation/injectivity over the normalized domain;
- target projection safety/completeness where claimed.

These are targets. No theorem is to be described as mechanically proved until the corresponding checked artifact is committed.
