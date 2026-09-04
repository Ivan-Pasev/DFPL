# DFPL N-0 §12 — Evidence Closure, Independent Encoder Reproduction, and N0-RC Adjudication

**Status:** Active evidence gate — 2026-09-04

## 12.0 Purpose
§12 is not another semantic expansion. It defines the adjudication procedure by which the N-0 freeze candidates may, or may not, become an N0-RC. Specification prose, repository presence and manually entered expected values are insufficient.

## 12.1 Constitutional input set
The candidate adjudication set consists of:

- DFPL normative §§0–11;
- `registry/n0-tag-registry.json`;
- `registry/n0-domain-registry.json`;
- `registry/n0-unicode-profile.json`;
- `registry/n0-kernel-descriptor.candidate.json`;
- `conformance/n0-corpus-manifest.json` and referenced vector packs;
- candidate release manifest;
- implementation and formal evidence reports when produced.

Any semantic change to this set resets affected evidence.

## 12.2 Evidence closure principle
For every mandatory vector, expected semantic result, canonical bytes and content ID are hypotheses until reproduced by an eligible implementation path. Evidence records observations; it does not rewrite expected results silently.

If implementation output differs from the candidate expectation, the vector is FAIL/PENDING_ADJUDICATION until one of the following is explicitly decided:

1. implementation defect;
2. vector defect;
3. normative specification ambiguity/defect;
4. profile mismatch;
5. unsupported-domain case.

Corrections create a new corpus/registry version where identity-sensitive data changes.

## 12.3 Implementation A
Implementation A is the reference-candidate path, presently expected to mature from `DFPL-LAB/frontend-rs`.

Before it can produce E2 evidence it MUST record:

- exact repository commit;
- Rust/toolchain and dependency lock state;
- host OS/architecture relevant to reproduction;
- deterministic invocation;
- executed vector IDs;
- stdout/stderr or structured report;
- generated artifact digests;
- pass/fail/skip status;
- supported-domain declaration.

Repository source alone is E0/E1 material, not E2.

## 12.4 Independent Implementation B
C3 N-0 RC adjudication requires an independently derived encoding path. Implementation B MUST NOT call, link or copy the canonical encoder implementation from A. Sharing the normative JSON registries and specification is permitted and required; sharing encoder logic defeats independence.

Preferred first B paths are:

- a small Python or other-language encoder written directly from §8 + registries; or
- a mechanized executable encoder derived from a formal model.

The evidence report MUST disclose shared dependencies and generation provenance.

## 12.5 Mandatory first reproduction subset
Before broad corpus completion, the following sentinel vectors MUST reproduce exactly:

- Bool false/true;
- empty/non-empty Bytes;
- ASCII and non-ASCII NFC Text;
- Int 0, ±1, values beyond 128-bit range;
- Option None/Some;
- List/Set/Map/Record ordering;
- Ref and LocalRef;
- one expression tree;
- every detailed Verdict constructor;
- one normalized LawIRBody;
- one KernelDescriptor/KernelID;
- one LawID;
- one DecisionCertificateBody/DecisionID.

The sentinel subset is necessary but not sufficient for N0-RC.

## 12.6 C0–C5 evidence campaign
Implementation A MUST execute the mandatory corpus for C0 Parse, C1 Static, C2 Normalize, C3 Encode/ID, C4 Evaluate and C5 Certificate.

An N0-RC candidate requires at least E2 reproducibility for C0–C5 under the declared supported domain. C3 additionally requires independent reproduction of the mandatory canonical-byte/ID subset.

Skipped mandatory vectors block promotion unless the release manifest narrows the claimed supported domain and §10 permits that narrowing.

## 12.7 Failure preservation
Failed outputs, crashes, divergent bytes, ambiguous diagnostics and unsupported cases MUST be retained as evidence. A rerun does not erase prior failures. The adjudication package records the lineage from failure to correction and rerun.

## 12.8 KernelID derivation gate
`kernel_id` MUST remain null while any KernelDescriptor field or bound registry identity is unresolved. KernelID may be populated only after:

1. descriptor structure is frozen;
2. all referenced registry/profile identities are fixed;
3. canonical descriptor encoding is implemented;
4. at least two eligible paths reproduce descriptor bytes and KernelID;
5. the exact evidence reports are referenced by the release candidate.

## 12.9 N0-RC decision
Adjudication result is one of:

- `HOLD_SPEC_DEFECT`
- `HOLD_CORPUS_INCOMPLETE`
- `HOLD_IMPLEMENTATION_FAILURE`
- `HOLD_REPRODUCTION_DIVERGENCE`
- `HOLD_EVIDENCE_INCOMPLETE`
- `PROMOTE_N0_RC`

`PROMOTE_N0_RC` is permitted only when all §10/§11 RC prerequisites and this section's reproduction gates are satisfied.

## 12.10 No automatic sealing
N0-RC is still not N0-SEALED. RC begins a stabilization/adversarial review period. Sealing requires the complete release-manifest gate, security/adversarial corpus, migration/compatibility declarations and closure of blockers required by §10.

## 12.11 Required evidence package
The adjudication package MUST contain:

- immutable source commit refs;
- machine-readable registries and descriptor;
- corpus manifest + vector pack digests;
- Implementation A evidence report;
- Implementation B C3 reproduction report;
- differential comparison report;
- failure/adjudication ledger;
- supported/unsupported domain statement;
- formal evidence references, if any;
- candidate release manifest;
- final adjudication record.

## 12.12 Current adjudication
As of 2026-09-04:

- machine-readable candidate registries exist;
- a candidate KernelDescriptor structure exists;
- the first cross-class vector pack exists;
- no complete C0–C5 E2 evidence report exists;
- no eligible independent C3 reproduction report exists;
- KernelID remains unset;
- N0-RC is therefore **not justified**.

Current result: `HOLD_EVIDENCE_INCOMPLETE`.

## 12.13 Property/evidence obligations
T-EVID-01 Evidence Non-Fabrication; T-EVID-02 Failure Preservation; T-EVID-03 Implementation Independence; T-EVID-04 Reproduction Determinism; T-EVID-05 Descriptor/KernelID Closure; T-EVID-06 Corpus Version Sensitivity; T-EVID-07 Supported-Domain Honesty; T-EVID-08 Differential Comparison Completeness; T-EVID-09 RC Gate Soundness; T-EVID-10 RC/Seal Separation.

## NEXT
Materialize the remaining mandatory vectors and execute Implementation A + independent Implementation B. Advance only from recorded evidence.