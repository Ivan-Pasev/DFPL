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
- [x] §9 Decision Certificates — freeze candidate
- [x] §10 Conformance, Security, Versioning, and Migration — freeze candidate
- [ ] §11 N-0 Registry Freeze, Machine-Readable Corpus, and Release Manifest — current

**N-0 is not sealed yet.** §10 makes sealing an evidence gate: exact registries, machine-readable corpus, reproducible C0–C5 implementation evidence, independently reproduced C3 bytes/IDs, published limitations/security assumptions and a content-addressed release manifest.

## Formalization

- [ ] Lean types and values
- [ ] Lean syntax and static semantics
- [ ] Canonical Law IR
- [ ] Normalization termination/idempotence
- [ ] Expression/Law evaluation determinism
- [ ] Decision-algebra projection proofs
- [ ] Canonical encoding properties
- [ ] Decision-certificate binding/projection properties
- [ ] Conformance/migration properties
- [ ] Projection obligations

## Experimental frontend / reference path

Private `DFPL-LAB/frontend-rs` remains experimental work against §§0–10:

- [x] S-expression parser scaffold
- [x] basic Canonical IR structures
- [x] deterministic clause normalization
- [x] duplicate ClauseID rejection
- [x] alpha-invariant `LocalRef {depth,slot,type}` representation
- [x] first normalization golden vector
- [x] §7 Verdict/VerdictClass structural prototype
- [x] initial §8 encoder scaffold for selected primitives
- [x] §9 DecisionCertificate structural prototype
- [ ] full DFPL-S0 lexer
- [ ] name/type/schema resolution
- [ ] phase/static checker
- [ ] complete normalization
- [ ] §6 evaluator prototype
- [ ] complete §8 canonical encoder
- [ ] exact N-0 tag/domain/Unicode registries
- [ ] machine-executable byte/hash/certificate corpus
- [ ] reproducible C0–C5/E2 build/test evidence
- [ ] independent C3 byte/ID reproduction

No public conformance claim exists yet. G2/E2 requires reproducible execution evidence, not repository presence alone.

## Public reference implementation

- [ ] Rust workspace promotion from DFPL-LAB
- [ ] parser
- [ ] static checker
- [ ] normalizer
- [ ] evaluator
- [ ] decision algebra
- [ ] canonical encoder
- [ ] certificate layer
- [ ] conformance report generator

Promotion requires private-lab evidence gates and conformance fixtures.

## Targets

- [ ] WASM differential conformance
- [ ] JavaScript adapter conformance
- [ ] EVM profiles after N-0 sealing

## PRIMA

- [x] §0 Orchestration boundary — freeze candidate
- [x] §1 PlanIR and Effect Algebra — freeze candidate
- [x] §2 Capability and Authorization Model — freeze candidate
- [x] §3 Effect Gateway and Outcome Semantics — freeze candidate
- [x] §4 Agent, Supervision, and Recursive Process Semantics — freeze candidate
- [x] §5 Runtime Profiles, Messaging, Scheduling, and Agent State Persistence — freeze candidate
- [x] §6 Runtime Conformance and Reference Profile — freeze candidate
- [x] §7 Runtime Artifact Identities, Event/Trace Model, and Cross-Runtime Handoff Conformance — freeze candidate
- [ ] §8 RP0 Machine-Readable Event/Handoff Corpus and Reference Runtime Execution Evidence — current

### RP0 reference-runtime implementation target

`PRIMA-RP0-DURABLE-MAILBOX-v1` is the first executable runtime claim surface:

- [ ] durable mailbox/store schema
- [ ] canonical MessageID/EventID/CheckpointID/HandoffID implementation
- [ ] stable MessageID + dedup
- [ ] atomic local acknowledgement transaction
- [ ] AgentState/checkpoint persistence
- [ ] replay/authorization consumption persistence
- [ ] budget persistence
- [ ] lease epoch acquisition/fencing
- [ ] execution-intent markers
- [ ] OutcomeReceipt / UnknownOutcome persistence
- [ ] deterministic mock effect adapter
- [ ] failure injector F0..F12
- [ ] machine-readable RP0 runtime/event/handoff vectors
- [ ] cross-runtime handoff harness
- [ ] R1 durable-local evidence
- [ ] R2 failure-recovery evidence

No RP0 conformance class is claimed until the corresponding vectors execute reproducibly.