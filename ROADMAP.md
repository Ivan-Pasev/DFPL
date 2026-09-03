# DFPL Roadmap

## DFPL-K normative closure

- [x] §0 Semantic boundary / conformance model — freeze candidate
- [x] §1 Canonical values and types — freeze candidate
- [x] §2 DFPL-S0 surface syntax — freeze candidate
- [x] §3 Static semantics / name resolution / phase typing — freeze candidate
- [x] §4 Canonical Law IR — freeze candidate
- [x] §5 Normalization — freeze candidate
- [x] §6 Dynamic semantics — freeze candidate
- [ ] §7 Detailed decision algebra — current
- [ ] §8 Canonical encoding and IDs
- [ ] §9 Decision Certificates
- [ ] §10 Conformance, security, versioning

## Formalization

- [ ] Lean types and values
- [ ] Lean syntax and static semantics
- [ ] Canonical Law IR
- [ ] Normalization termination/idempotence
- [ ] Expression/Law evaluation determinism
- [ ] Canonical encoding properties
- [ ] Projection obligations

## Experimental frontend / reference path

Private `DFPL-LAB/frontend-rs` has begun as G1 experimental work against §§0–6:

- [x] S-expression parser scaffold
- [x] basic Canonical IR structures
- [x] deterministic clause normalization
- [x] duplicate ClauseID rejection
- [x] alpha-invariant `LocalRef {depth,slot,type}` representation
- [x] first normalization golden vector
- [ ] full DFPL-S0 lexer
- [ ] name/type/schema resolution
- [ ] phase/static checker
- [ ] complete normalization
- [ ] §6 evaluator prototype
- [ ] reproducible build/test evidence

No public conformance claim exists yet.

## Public reference implementation

- [ ] Rust workspace promotion from DFPL-LAB
- [ ] parser
- [ ] static checker
- [ ] normalizer
- [ ] evaluator
- [ ] canonical encoder
- [ ] certificate layer

Promotion requires private-lab evidence gates and conformance fixtures.

## Targets

- [ ] WASM differential conformance
- [ ] JavaScript adapter conformance
- [ ] EVM profiles after kernel closure

## PRIMA

- [x] §0 Orchestration boundary — freeze candidate
- [x] §1 PlanIR and Effect Algebra — freeze candidate
- [x] §2 Capability and Authorization Model — freeze candidate
- [x] §3 Effect Gateway and Outcome Semantics — freeze candidate
- [ ] §4 Agent, Supervision, and Recursive Process Semantics — current
- [ ] runtime/profile conformance
