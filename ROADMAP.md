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
- [x] §12 Evidence Closure / N0-RC Adjudication — evidence gate defined
- [x] §13 Executable Evidence Campaign / RC-or-Redesign checkpoint — active execution campaign

**Current N-0 adjudication: `HOLD_EVIDENCE_INCOMPLETE`.** N-0 remains unsealed and is not N0-RC. The project now has real executable evidence, but only for scoped subsets.

## Immediate N-0 evidence campaign

- [x] candidate tag/domain/Unicode registries
- [x] candidate machine-readable KernelDescriptor structure
- [x] N-0 corpus manifest bound to descriptor
- [x] first materialized C0–C5 vector pack
- [x] independent Python Implementation B sentinel encoder
- [x] repeated B E2 execution for primitive/Int/NFC sentinel subset
- [x] repeated Rust Implementation A CI/cargo-test execution for current G1 subset
- [x] eight primitive/Int/ASCII C3 sentinels independently matched A↔B — `DIFFERENTIAL_E3`
- [ ] exact Unicode-profile reproduction in A and B
- [ ] complete mandatory vector set
- [ ] full C0 parser campaign
- [ ] C1 name/type/schema/phase checker campaign
- [ ] complete C2 normalization campaign
- [ ] complete C3 composite/type/ref/expression/LawIR/ID/decoder campaign
- [ ] C4 evaluator campaign
- [ ] C5 certificate campaign
- [ ] derive/reproduce KernelDescriptor bytes and KernelID
- [ ] derive/reproduce LawID and DecisionID
- [ ] N0-RC adjudication package

Evidence:
- `evidence/encoder-b-e2-2026-09-04.json`
- `evidence/c3-sentinel-differential-e3-2026-09-04.json`
- private A report: `DFPL-LAB/evidence/frontend-rs-a-e2-2026-09-04.json`

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

Private `DFPL-LAB/frontend-rs` remains **G1 experimental**. It now has reproducible CI evidence over its current subset; that does not make it a full DFPL implementation or G2 automatically.

- [x] S-expression parser scaffold
- [x] basic Canonical IR structures
- [x] deterministic clause normalization
- [x] duplicate ClauseID rejection
- [x] alpha-invariant `LocalRef {depth,slot,type}` representation
- [x] §7 Verdict/VerdictClass structural prototype
- [x] primitive §8 encoder including arbitrary-precision candidate Int encoding
- [x] §9 DecisionCertificate structural prototype
- [x] G1 registry mirror
- [x] reproducible GitHub Actions `cargo test` over current G1 suite
- [ ] full DFPL-S0 lexer
- [ ] name/type/schema resolution
- [ ] phase/static checker
- [ ] complete normalization
- [ ] full §6 evaluator
- [ ] complete §8 canonical encoder
- [ ] descriptor encoder/KernelID derivation
- [ ] full C0–C5/E2 evidence

## Public reference implementation

- [ ] Rust workspace promotion from DFPL-LAB
- [ ] parser/static checker/normalizer/evaluator
- [ ] complete decision/canonical encoder/certificate layer
- [ ] conformance report generator

Promotion requires the private-lab gates and corpus evidence.

## Targets

- [x] first independent second encoder path — scoped Python B sentinel implementation
- [ ] complete independent C3 encoder
- [ ] WASM differential conformance
- [ ] JavaScript adapter conformance
- [ ] EVM profiles after N-0 sealing

## PRIMA

- [x] §§0–8 freeze candidates
- [x] §9 RP0 adjudication gate defined
- [x] §10 Executable RP0 Campaign checkpoint — active execution campaign

**Current RP0 adjudication: `HOLD_HARNESS_INCOMPLETE`.** No R1/R2 claim exists.

### RP0 reference-runtime evidence campaign

- [x] materialized public F0–F12 candidate vector pack
- [x] private deterministic persisted-state G1 model
- [x] first single-environment RP0 model campaign — 9/9 tests PASS, all F0–F12 executable
- [ ] real transactional durable mailbox/store Backend A
- [ ] stable canonical runtime artifact IDs in the real harness
- [ ] atomic local acknowledgement transaction
- [ ] AgentState/checkpoint/replay/authorization/budget durable stores
- [ ] lease/fencing implementation
- [ ] execution-intent + OutcomeReceipt/UnknownOutcome persistence
- [ ] deterministic mock effect adapter integrated with durable store
- [ ] process-style crash/reopen F0–F12 campaign
- [ ] Backend A reproduced campaign
- [ ] Backend B reproduction
- [ ] cross-runtime handoff harness
- [ ] R1 durable-local PASS_REPRODUCED evidence
- [ ] R2 failure-recovery PASS_REPRODUCED evidence

The passing G1 model is executable design evidence, not RP0 runtime conformance.