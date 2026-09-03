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

## Current maturity

Current N-0 freeze candidates:

1. §0 Semantic Boundary / Conformance Model
2. §1 Canonical Value Domain and Type System
3. §2 DFPL-S0 Surface Syntax
4. §3 Static Semantics / Name Resolution / Phase Typing

**Current NEXT:** §4 Canonical Law IR.

PRIMA currently has §0 Orchestration Boundary as a freeze candidate.

**Current PRIMA NEXT:** §1 PlanIR and Effect Algebra.

The project does not yet claim complete formal proof, complete target conformance, production deployment, or automatic legal force.

## Prime separations

- Law != Effect
- Semantic Permit != Authorization
- Authorization != Execution
- Hash/commitment != Proof
- Identity != Authority
- Simulation != Deployment
- Specification != Implementation

## Repository structure

- `spec/` — normative DFPL-K draft
- `prima/` — orchestration architecture
- `formal/` — proof/mechanization work
- `reference/` — reference implementation
- `targets/` — target/runtime projections
- `profiles/` — optional integration profiles
- `conformance/` — golden, differential, property, fuzz and adversarial corpus
- `examples/` — DFPL examples
- `docs/` — architecture, manuscript and White Paper surfaces
- `omega/` — portable LLM bootstrap

See `ROADMAP.md` for the current implementation sequence.
