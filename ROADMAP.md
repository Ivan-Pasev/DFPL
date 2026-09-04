# DFPL Roadmap

## DFPL-K normative closure

- [x] §0 Semantic boundary / conformance model — freeze candidate
- [x] §1 Canonical values and types — freeze candidate
- [x] §2 DFPL-S0 surface syntax — freeze candidate
- [x] §3 Static semantics / name resolution / phase typing — freeze candidate
- [x] §4 Canonical Law IR — freeze candidate
- [x] §5 Normalization — freeze candidate
- [x] §6 Dynamic semantics — freeze candidate
- [x] §7 Detailed decision algebra — freeze candidate
- [x] §8 Canonical encoding and IDs — freeze candidate
- [ ] §9 Decision Certificates — current
- [ ] §10 Conformance, security, versioning

## Formalization

- [ ] Lean types and values
- [ ] Lean syntax and static semantics
- [ ] Canonical Law IR
- [ ] Normalization termination/idempotence
- [ ] Expression/Law evaluation determinism
- [ ] Decision-algebra projection proofs
- [ ] Canonical encoding properties
- [ ] Projection obligations

## Experimental frontend / reference path

Private `DFPL-LAB/frontend-rs` remains G1 experimental work against §§0–8:

- [x] S-expression parser scaffold
- [x] basic Canonical IR structures
- [x] deterministic clause normalization
- [x] duplicate ClauseID rejection
- [x] alpha-invariant `LocalRef {depth,slot,type}` representation
- [x] first normalization golden vector
- [x] §7 Verdict/VerdictClass structural prototype
- [ ] full DFPL-S0 lexer
- [ ] name/type/schema resolution
- [ ] phase/static checker
- [ ] complete normalization
- [ ] §6 evaluator prototype
- [ ] §8 canonical encoder prototype
- [ ] machine-executable byte/hash golden vectors
- [ ] reproducible build/test evidence

No public conformance claim exists yet. G2 requires reproducible execution evidence, not repository presence alone.

## Public reference implementation

- [ ] Rust workspace promotion from DFPL-LAB
- [ ] parser
- [ ] static checker
- [ ] normalizer
- [ ] evaluator
- [ ] decision algebra
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
- [x] §4 Agent, Supervision, and Recursive Process Semantics — freeze candidate
- [x] §5 Runtime Profiles, Messaging, Scheduling, and Agent State Persistence — freeze candidate
- [ ] §6 Runtime Conformance and Reference Profile — current
