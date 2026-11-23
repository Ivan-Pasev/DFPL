# DFPL — Digital Fabrica Programming Language

DFPL is a specification-first cybernetic programming architecture centered on a deterministic semantic kernel for evaluating admissible candidate state transitions under explicit constraints, invariants, schemas, and evidence.

The architecture has two distinct spines:

- **DFPL-K** — the pure semantic kernel.
- **PRIMA** — the recursive/effectful orchestration plane that produces finite plans, requests DFPL-K verification, passes explicit authorization/capability gates, executes effects, and records outcomes.

Canonical chain:

`Intent → PlanIR → CandidateTransition → EvidenceIR → DFPL-K → SemanticVerdict → DecisionCertificate → Authorization → EffectGateway → OutcomeReceipt`

## Project authority

The authoritative manuscript and continuity working tree is:

https://drive.google.com/drive/folders/1wK7MNoIxU3HvxQ6ciA94D8pvvfhT0juW

GitHub is the public specification, implementation, conformance, and release surface. Frozen GitHub releases should identify the canonical source state from which they were generated.

## Current maturity and evidence boundaries

- **DFPL-K N-0:** normative draft §§0–11 and evidence/adjudication §§12–13 are present. Current adjudication is **`HOLD_EVIDENCE_INCOMPLETE`**: N-0 is unsealed and is not N0-RC. A and B have reproduced eight candidate C3 sentinel byte encodings (`DIFFERENTIAL_E3` for that *bounded subset*), not the full C0–C5 conformance campaign. `KernelID` remains withheld.
- **PRIMA RP0:** §§0–8 orchestration candidates and §§9–10 adjudication/executable-campaign records are present. The F0–F12 vector pack and a private deterministic persisted-state model have evidence, but the real durable Backend A/B campaign remains open. Current adjudication is **`HOLD_HARNESS_INCOMPLETE`**; no R1/R2 claim.
- **Implementation maturity:** `tools/independent_encoder_b.py` and its source-local tests exercise a limited Python B encoding path. The broader reference implementation remains experimental in a separate private lab, not a verified public full runtime.

**Next evidence gates:** expand independent A/B differential encoding and full C0–C5 coverage for DFPL-K; implement and reproduce real transactional durable Backend A/B RP0 evidence for PRIMA. See [ROADMAP.md](ROADMAP.md), [DFPL §13](spec/13-executable-evidence-campaign.md), and [PRIMA §10](prima/10-executable-rp0-campaign.md) for the exact open obligations.

The project does not yet claim complete formal proof, complete target conformance, production deployment, security certification or automatic legal force.

## Prime separations

- Law != Effect
- Semantic Permit != Authorization
- Authorization != Execution
- Hash/commitment != Proof
- Identity != Authority
- Simulation != Deployment
- Specification != Implementation

## Repository structure

**Present in this public repository:**

- `spec/` — DFPL-K normative drafts and evidence gates
- `prima/` — PRIMA orchestration, RP0 vectors and executable-campaign contracts
- `formal/` — formalization planning; not a complete mechanized proof
- `conformance/` — candidate N-0 corpus and scoped vectors
- `registry/` — candidate tag/domain/Unicode registries and KernelDescriptor
- `releases/` — **candidate** release manifest; not a sealed release
- `evidence/` — retained scoped encoder/differential observations
- `tools/` and `tests/` — independent Python encoder B and its test surface
- `examples/` and `docs/` — illustrative examples and architecture
- `.github/workflows/` — bounded encoder B workflow, not whole-project conformance CI

**Architectural destinations, not present source directories:** `reference/`, `targets/`, `profiles/`, `omega/`. Their intended roles do not imply shipped implementations.

## Rights and contribution boundary

A root `LICENSE` file is **not present** in this source-locked snapshot. Public visibility does not itself grant broad copyright reuse rights. Do not infer a software redistribution license, upstream endorsement, or permission to transfer private-lab code. License selection and publication of additional implementation code require their own steward review. See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).

See [ROADMAP.md](ROADMAP.md) for the current implementation sequence.
