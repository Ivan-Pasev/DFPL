# DFPL N-0 §11 — Registry Freeze, Machine-Readable Corpus, and Release Manifest

**Status:** Freeze candidate — 2026-09-04

## Purpose
§11 converts §§0–10 from prose-defined freeze candidates into named machine-readable constitutional inputs. It freezes the candidate N-0 registry layout, corpus manifest format and release-manifest contract while keeping N-0 unsealed until reproducible evidence exists.

## N-0 registry set
The N-0 candidate KernelDescriptor MUST bind content identities for at least:

- `registry/n0-tag-registry.json`
- `registry/n0-domain-registry.json`
- `registry/n0-unicode-profile.json`
- grammar/type/normalization/LawIR/dynamic/decision profile IDs
- hash algorithm profile (`SHA-256` baseline)
- canonical encoding profile ID

Registry files are normative data once included by digest in a sealed KernelDescriptor. Editing a bound registry creates different descriptor bytes and therefore a different KernelID.

## Tag registry discipline
N-0 uses one-byte tags. Every assigned tag has exactly one constructor meaning inside its registry version. Reuse with different meaning is forbidden. Unassigned values are reserved and MUST be rejected by N-0 decoders. Tag classes are grouped by range for readability only; the numeric byte is authoritative.

## Domain registry discipline
Every content-ID family has one exact ASCII/UTF-8 byte literal ending in `0x00`. Domain literals are compared byte-for-byte. Human spelling variants are not aliases. Hashing an object under the wrong domain is an identity error, not compatibility.

## Unicode profile
N-0 Text/Identifier processing is pinned by one machine-readable Unicode profile specifying Unicode version, normalization form, UTF-8 transport, forbidden scalar conditions and identifier restrictions. Host-default locale/case/transliteration behavior is excluded.

## Corpus object
`N0CorpusManifest` binds:

`{corpus_version, kernel_descriptor_ref, registry_refs[], vector_families[], vector_refs[], required_classes[], known_gaps[], corpus_digest}`.

Vector records bind `{vector_id, class, object_kind, input_refs, expected_result, expected_bytes_hex?, expected_id_hex?, expected_error?, status, provenance}`.

The corpus MUST be deterministic and content-addressed. Vector ordering is canonical by `vector_id` UTF-8 bytes after N-0 normalization.

## Mandatory corpus families
At minimum:

1. parser accept/reject;
2. static/type/phase errors;
3. normalization equivalence/rejection;
4. primitive values including very large positive/negative Int;
5. Unicode Text/identifier cases;
6. List/Set/Map/Record canonical ordering and duplicates;
7. Ref/LocalRef and alpha invariance;
8. expression evaluation and short-circuit/error order;
9. all detailed Verdict constructors and coarse classes;
10. canonical type/expression/LawIR bytes;
11. KernelID/LawID vectors;
12. DecisionCertificate construction/tamper vectors;
13. noncanonical decoder rejection;
14. SupportedDomain/ResourceLimit cases;
15. each claimed target/projection profile.

## Vector status
Machine-readable vectors use one of:

- `DRAFT_UNVERIFIED`
- `CANDIDATE_SINGLE_IMPLEMENTATION`
- `REPRODUCED_E2`
- `DIFFERENTIAL_E3`
- `MECHANIZED_E4` where applicable
- `RETIRED`

A vector does not become normative evidence merely because expected bytes were typed into a file.

## Independent reproduction
C3 sealing requires at least two independently implemented encoding paths, or one implementation plus an independently derived/mechanized encoder, to reproduce the exact mandatory byte/ID subset. Shared helper code that trivially reuses the same encoder does not establish independence.

## Release manifest
`N0ReleaseManifest` binds:

`{release_label, kernel_descriptor_ref, kernel_id, normative_spec_refs[], registry_refs[], corpus_ref, implementation_evidence[], formal_evidence[], security_assumptions[], unsupported_domains[], compatibility_migrations[], known_open_obligations[], supersedes?, release_manifest_id}`.

`release_manifest_id` is excluded from its own body hash and is derived under a dedicated release-manifest domain.

## Release states
- **PRE-N0** — architecture/spec work; not release-conformant.
- **N0-FREEZE-CANDIDATE** — §§0–11 and candidate registries/corpus exist.
- **N0-RC** — mandatory registry/corpus fixed; at least one C0–C5 E2 implementation and independent mandatory C3 reproduction exist; unresolved blockers listed explicitly.
- **N0-SEALED** — §10 gate fully satisfied and manifest content-addresses all release evidence.

State names do not override evidence.

## Change control
Any candidate registry/corpus correction before sealing increments its registry/corpus version and invalidates stale expected IDs as applicable. After N0-SEALED, normative changes require a successor KernelID/release lineage rather than in-place mutation.

## Conformance evidence report
A machine-readable evidence report binds implementation commit, toolchain/environment, supported domain, claimed C-classes/E-level, corpus digest, executed vector IDs, pass/fail/skip results, command transcript or reproducible invocation, generated artifact digests and known exclusions.

## Property targets
T-REG-01 Tag Uniqueness; T-REG-02 Reserved-Tag Rejection; T-REG-03 Domain Uniqueness; T-REG-04 Registry Descriptor Sensitivity; T-CORP-01 Corpus Ordering Determinism; T-CORP-02 Vector Identity Stability; T-CORP-03 Evidence/Expected-Value Separation; T-REL-01 Release Manifest Non-Self-Reference; T-REL-02 Release Evidence Closure; T-REL-03 Sealed-Lineage Immutability.

These remain obligations until evidenced.

## Freeze consequence
The N-0 specification now has a candidate machine-readable constitutional boundary. The next work is implementation and independent reproduction, not another semantic redesign.

## NEXT
§12 — Evidence Closure, Independent Encoder Reproduction, and N0-RC Adjudication.