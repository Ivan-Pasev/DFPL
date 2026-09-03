# Ω-DFPL §0 — Semantic Boundary and Conformance Model

**Status:** normative draft / freeze candidate

DFPL-K is a versioned semantic system rather than a particular runtime or implementation.

`K_DFPL = (G,T,N,IR,C,S,D)`

- `G` grammar
- `T` static semantics and type system
- `N` normalization
- `IR` Canonical Law/Transition IR
- `C` canonical encoding
- `S` dynamic semantics
- `D` decision algebra

Core evaluation:

`Evaluate_K(L, pre_state, candidate_post_state, evidence) -> SemanticVerdict`

## Prime requirements

- semantic authority belongs to the normative specification;
- every conformance claim is relative to a Kernel ID/profile/class;
- sealed Kernel versions are immutable;
- all decision-relevant information is explicit;
- semantic evaluation performs no external effects;
- metadata/provenance cannot silently change semantics;
- identity, authentication, capability, legal authority, and execution remain distinct;
- `Invalid != Deny`;
- commitment/hash != semantic proof;
- implementation status requires executable evidence.

`Decision != Effect`.
