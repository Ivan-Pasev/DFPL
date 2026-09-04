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
- [x] §11 N-0 Registry Freeze, Machine-Readable Corpus, and Release Manifest — freeze candidate
- [x] §12 Evidence Closure, Independent Encoder Reproduction, and N0-RC Adjudication — evidence gate defined

**Current N-0 adjudication: `HOLD_EVIDENCE_INCOMPLETE`.** N-0 remains unsealed and is not N0-RC. Candidate registries, a machine-readable KernelDescriptor structure, corpus manifest and first cross-class vector pack now exist; reproducible C0–C5 E2 and independent C3 reproduction do not.

## Immediate N-0 evidence campaign

- [x] candidate tag/domain/Unicode registries
- [x] candidate machine-readable KernelDescriptor structure
- [x] N-0 corpus manifest bound to descriptor
- [x] first materialized C0–C5 vector pack
- [ ] freeze complete mandatory vector set
- [ ] complete §8 encoder in Implementation A
- [ ] execute reproducible C0–C5 campaign
- [ ] produce machine-readable Implementation A evidence report
- [ ] build independent Implementation B encoder
- [ ] reproduce mandatory C3 bytes/IDs independently
- [ ] derive/reproduce KernelDescriptor bytes and KernelID
- [ ] differential comparison/adjudication ledger
- [ ] N0-RC adjudication package

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
- [ ] Registry uniqueness/domain separation properties
- [ ] Evidence-gate soundness properties

## Experimental frontend / reference path

Private `DFPL-LAB/frontend-rs` remains experimental against §§0–12. Repository source is not execution evidence.

- [x] S-expression parser scaffold
- [x] basic Canonical IR structures
- [x] deterministic clause normalization
- [x] duplicate ClauseID rejection
- [x] alpha-invariant `LocalRef {depth,slot,type}` representation
- [x] first normalization golden vector
- [x] §7 Verdict/VerdictClass structural prototype
- [x] initial §8 encoder scaffold for selected primitives
- [x] §9 DecisionCertificate structural prototype
- [x] G1 mirror of candidate tag/domain registry constants
- [ ] full DFPL-S0 lexer
- [ ] name/type/schema resolution
- [ ] phase/static checker
- [ ] complete normalization
- [ ] §6 evaluator prototype
- [ ] complete §8 canonical encoder
- [ ] descriptor encoder/KernelID derivation
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

- [ ] independent second encoder path
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
- [x] §8 RP0 Machine-Readable Event/Handoff Corpus and Reference Runtime Execution Evidence — freeze candidate
- [x] §9 RP0 Reference Runtime Adjudication, Cross-Backend Reproduction, and Promotion Decision — evidence gate defined

**Current RP0 adjudication: `HOLD_HARNESS_INCOMPLETE`.** No R1/R2 claim exists.

### RP0 reference-runtime evidence campaign

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
- [x] public RP0 corpus manifest skeleton
- [ ] materialized F0..F12 vectors
- [ ] Backend A reproducible campaign
- [ ] Backend B reproduction
- [ ] cross-runtime handoff harness
- [ ] R1 durable-local PASS_REPRODUCED evidence
- [ ] R2 failure-recovery PASS_REPRODUCED evidence

No RP0 conformance class is claimed until the corresponding vectors execute reproducibly.