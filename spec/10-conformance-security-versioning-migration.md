# DFPL N-0 §10 — Conformance, Security, Versioning, and Migration

**Status:** Freeze candidate — 2026-09-04

## Purpose
§10 defines the conditions under which an implementation, projection, certificate verifier, package or release may claim conformance to a sealed DFPL Kernel. It also defines security-claim boundaries, compatibility/migration relations, and the evidence gate for an N-0 release.

## Conformance claim tuple
Every public claim identifies:

`{kernel_id, implementation_id/version/commit, conformance_class, supported_domain, profile_set, corpus_version, evidence_ref}`.

Unqualified “DFPL compatible” or “fully conformant” claims are invalid.

## Classes
- **C0-PARSE** — §2 source acceptance/rejection and AST.
- **C1-STATIC** — §3 resolution/type/phase/well-formedness.
- **C2-NORMALIZE** — same canonical LawIRBody or explicit normalization failure.
- **C3-ENCODE** — exact canonical bytes and content IDs over `Supported_t`.
- **C4-EVALUATE** — exact detailed Verdict and VerdictClass.
- **C5-CERTIFICATE** — §9 certificate construction/verification.
- **C6-FULL-KERNEL** — C0–C5 over the declared domain and mandatory corpus.

Narrower claims must not imply higher classes.

## Unsupported domain
An implementation unable to represent/resource a valid Kernel object returns explicit `UnsupportedDomain` or `ResourceLimit`. It must not truncate, wrap, round, substitute, weaken, silently normalize differently or reinterpret. `Unsupported != Invalid != Deny`.

## Normative corpus
The versioned, content-addressed N-0 corpus covers parser/static behavior, normalization/rejection, arbitrary-precision integers, Unicode, collection ordering/duplicates, alpha invariance, short-circuit/error order, all Verdict constructors/classes, canonical bytes/IDs, certificate tamper cases, resource/unsupported cases and every claimed projection profile.

## Evidence levels
- **E0 DOCUMENTED** — architecture/spec only.
- **E1 IMPLEMENTED** — reviewable code exists.
- **E2 REPRODUCED** — declared build/test commands reproduce results.
- **E3 DIFFERENTIAL** — at least two independent implementations reproduce applicable canonical vectors.
- **E4 MECHANIZED** — applicable formal obligations are checked by declared proof artifacts/toolchains.

Evidence level and conformance class are orthogonal.

## Security boundary
DFPL-K assumes declared cryptographic primitives, canonical parser/decoder rejection, artifact integrity and explicit trust profiles. It does not itself provide secrecy, endpoint authentication, key custody, side-channel resistance, Byzantine consensus, availability, legal authority, truthful sensors/oracles or safe external execution.

Adversarial testing includes malformed/truncated encodings, unknown tags, duplicate/unsorted structures, Unicode edge cases, large integer/depth resource attacks, domain confusion, certificate substitution/tampering, replay mismatch, fuzzing and metamorphic testing.

## Compatibility
`Compat(K_source,K_target,profile)` is explicit and directional. Initial relation classes:

`Exact | AcceptancePreserving | SafetyRefinement | DiagnosticCompatible | Migratable(profile) | Incompatible`.

Different KernelIDs do not alone establish incompatibility.

## Migration
A Law never changes in place under one LawID.

`MigrateLaw_{K1→K2}(LawArtifact)` returns a new target LawArtifact plus `MigrationWitness`, or explicit failure. The witness binds source/target KernelIDs and LawIDs, migration profile/version, canonical commitments, claimed relation and verification evidence.

State/evidence migration is typed. A DecisionCertificate remains a statement under its original KernelID/profile. Authorization does not automatically migrate with semantic artifacts.

## Versioning and deprecation
A sealed KernelDescriptor/KernelID is immutable. Normative changes to G/T/N/IR/C/S/D, Unicode policy, tag registry, hash/domain registry or mandatory conformance semantics create a new KernelID. Editorial non-semantic publication revisions may retain it. Human semver labels are aliases; KernelID is content-bound authority.

Deprecation does not mutate old kernels or artifacts. Runtimes explicitly declare accepted KernelIDs.

## N-0 release gate
N-0 becomes a sealed release only when:
1. §§0–10 contain no unresolved normative placeholders;
2. KernelDescriptor/tag/domain/Unicode registries are frozen;
3. mandatory corpus is machine-readable;
4. at least one implementation reaches declared C0–C5 with E2 reproducibility over its supported domain;
5. C3 canonical bytes/IDs are independently reproduced;
6. known deviations, unsupported domains and security assumptions are published;
7. proof obligations are labeled proved/open accurately; and
8. a content-addressed release manifest binds spec, corpus and evidence.

Until then N-0 remains a freeze candidate.

## Release manifest
`N0ReleaseManifest` binds release label, KernelID/Descriptor, normative document digests, corpus ID/version, reference implementation commits, evidence reports, formal-proof status, security/compatibility notes, known limitations and migration/supersession links.

## Property targets
T-CONF-01 Claim Scope Soundness; T-CONF-02 Unsupported-Domain Non-Approximation; T-CONF-03 Corpus Determinism; T-CONF-04 Cross-Implementation Byte Agreement; T-CONF-05 Compatibility Directionality; T-CONF-06 Migration Identity Separation; T-CONF-07 Certificate Kernel Preservation; T-CONF-08 Version Immutability; T-CONF-09 Release Manifest Binding; T-CONF-10 Security-Claim Non-Escalation.

These remain obligations until evidenced.

## Freeze consequence
DFPL-K now has a candidate N-0 constitutional boundary from source syntax through canonical semantic result and certificate to conformance, versioning and migration. **Sealing N-0 is an evidence gate, not a documentation declaration.**

## NEXT
§11 — N-0 Registry Freeze, Machine-Readable Corpus, and Release Manifest.