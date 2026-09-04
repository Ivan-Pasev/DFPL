# DFPL N-0 §13 — Executable Evidence Campaign and RC/Redesign Decision

**Status:** Active execution campaign — 2026-09-04

## 13.0 Purpose
§13 records executable observations against the §12 adjudication gate. It does not change DFPL semantics. Where an implementation diverges from the candidate constitution, the result is evidence for repair or redesign rather than permission to reinterpret the specification silently.

## 13.1 First reproducible implementation evidence
Implementation A (`Ivan-Pasev/DFPL-LAB/frontend-rs`) now has reproducible GitHub Actions execution on Ubuntu 24.04.4 with Rust/Cargo 1.98.0. The current sentinel-emitting commit `19ee1da1b759f8924c817722603b2a82ade9c4bc` passed 14 tests on two workflow attempts. A prior failing implementation commit is preserved in the private evidence lineage.

Implementation B (`tools/independent_encoder_b.py`) is an independently derived Python encoder built from public §8 + public registries without importing/linking A's Rust encoder. Its sentinel suite reproduced on GitHub Actions using Python 3.12.3.

These are scoped implementation observations, not C6 or N0-RC claims.

## 13.2 First differential C3 evidence
A and B independently reproduced identical candidate bytes for eight sentinel vectors:

- Bool false: `0100`
- Bool true: `0101`
- Bytes `aabb`: `030000000000000002aabb`
- ASCII Text `A`: `04000000000000000141`
- Int `0`: `02000000000000000000`
- Int `1`: `0200000000000000000101`
- Int `-1`: `0201000000000000000101`
- Int `2^128`: `020000000000000000110100000000000000000000000000000000`

Those vectors are therefore `DIFFERENTIAL_E3` for the exact exercised candidate subset.

NFC Text `é` / `e + combining acute` is only `REPRODUCED_E2` through B because A does not yet implement the Kernel-pinned Unicode normalization profile.

## 13.3 Evidence artifacts
Public evidence includes:

- `evidence/encoder-b-e2-2026-09-04.json`
- `evidence/c3-sentinel-differential-e3-2026-09-04.json`
- `conformance/vectors/n0-core-candidate-0001.json`

Private evidence includes the exact A run/toolchain/failure lineage in `DFPL-LAB/evidence/frontend-rs-a-e2-2026-09-04.json`.

## 13.4 What remains outside the differential subset
The following remain mandatory before C3 can be treated as complete:

- exact Unicode 15.1/NFC implementation/table pinning in both eligible paths;
- Option/List/Set/Map/Record encodings;
- Ref/LocalRef;
- normalized types;
- representative and complete expression constructors;
- every detailed Verdict payload encoding;
- complete LawIRBody;
- KernelDescriptor canonical encoding and KernelID;
- LawID;
- DecisionCertificateBody and DecisionID;
- noncanonical decoder rejection;
- malformed length/tag/ordering cases.

## 13.5 C0–C5 state
Current evidence does not establish full C0–C5 E2. The Rust laboratory has parser/normalization/decision/encoding unit scaffolds, but the public mandatory C0 parser, C1 static/phase, C2 normalization, C4 evaluator and C5 certificate vectors are not yet executed as one versioned conformance campaign.

## 13.6 KernelID remains withheld
`registry/n0-kernel-descriptor.candidate.json` still has `kernel_id = null`. This is required while descriptor canonical encoding and all bound identity-sensitive profiles have not yet been independently reproduced.

## 13.7 Current N0 adjudication
The existence of first E2/E3 evidence narrows the blocker but does not satisfy §12 RC criteria.

Current result remains:

`HOLD_EVIDENCE_INCOMPLETE`

Reasons:

1. mandatory C0–C5 corpus is incomplete;
2. C3 differential coverage is only a sentinel subset;
3. KernelDescriptor/KernelID are not reproduced;
4. complete LawIR/LawID and DecisionID vectors are absent;
5. Unicode table/version reproduction is incomplete;
6. full supported-domain and adversarial reports are absent.

## 13.8 Decision rule from here
Every next campaign cycle MUST terminate in one of:

- evidence-compatible implementation advance;
- implementation defect + repair;
- corpus defect + versioned correction;
- specification ambiguity/defect + explicit redesign;
- unsupported-domain declaration;
- promotion only when the complete gate is satisfied.

Evidence is never discarded merely because a later run passes.

## 13.9 Next executable target
Expand the A/B differential encoder through composite values, refs/types/expressions and canonical LawIR, then derive KernelDescriptor bytes/KernelID. In parallel execute the public C0/C1/C2/C4/C5 vectors through A and produce one machine-readable C0–C5 evidence report.

**NEXT:** §14 — KernelID/LawID Reproduction and Full C0–C5 Adjudication, only after the executable targets above produce evidence.