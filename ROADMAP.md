# DFPL Roadmap

## DFPL-K normative closure

- [x] §0 Semantic boundary / conformance model — freeze candidate
- [x] §1 Canonical values and types — freeze candidate
- [x] §2 DFPL-S0 surface syntax — freeze candidate
- [x] §3 Static semantics / name resolution / phase typing — freeze candidate
- [x] §4 Canonical Law IR — freeze candidate
- [x] §5 Normalization — freeze candidate
- [ ] §6 Dynamic semantics — current
- [ ] §7 Detailed decision algebra
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

## Reference implementation

- [ ] Rust workspace
- [ ] parser
- [ ] static checker
- [ ] normalizer
- [ ] evaluator
- [ ] canonical encoder
- [ ] certificate layer

Implementation starts experimentally in `DFPL-LAB` after the relevant normative interface stabilizes, then promotes through evidence gates.

## Targets

- [ ] WASM differential conformance
- [ ] JavaScript adapter conformance
- [ ] EVM profiles after kernel closure

## PRIMA

- [x] §0 Orchestration boundary — freeze candidate
- [x] §1 PlanIR and Effect Algebra — freeze candidate
- [x] §2 Capability and Authorization Model — freeze candidate
- [ ] §3 Effect Gateway and Outcome Semantics — current
- [ ] agent/supervision semantics
- [ ] runtime/profile conformance
