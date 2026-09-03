# DFPL / PRIMA Canonical Architecture

DFPL separates semantic verification from orchestration and effects.

## Kernel

`DFPL-K = (G,T,N,IR,C,S,D)`

- `G` grammar
- `T` static semantics and type system
- `N` normalization
- `IR` Canonical Law IR
- `C` canonical encoding
- `S` dynamic semantics
- `D` decision algebra

`Evaluate_K(Law, pre_state, candidate_post_state, evidence) -> SemanticVerdict`

## Orchestration

PRIMA lowers recursive/effectful intent into a finite `PlanIR` and binds it to a candidate transition, policy, evidence, capabilities, and replay context.

## Closed control loop

`Observe → Propose → Verify → Authorize → Act → Observe`

Expanded:

`Intent → PlanIR → CandidateTransition → EvidenceIR → DFPL-K → SemanticVerdict → DecisionCertificate → Authorization → EffectGateway → OutcomeReceipt`

## Architectural invariants

- Semantic evaluation performs no external effects.
- All decision-relevant information is explicit.
- Metadata does not silently alter Law semantics.
- A sealed Kernel version is immutable.
- Law identity, package provenance, operator identity, cryptographic authentication, authorization, and execution are distinct layers.
- Plan mutation requires fresh authorization.
- The Plan executed must be the Plan authorized.
- Divergence between proposed and observed effects is explicit.

## Public/private development split

The public `DFPL` repository is the standards, formalization, reference implementation, conformance, examples, and release surface.

The private `DFPL-LAB` repository is the experimental R&D surface. Promotion to the public repository requires explicit review and evidence.

Canonical continuity remains in the Google Drive working tree:

https://drive.google.com/drive/folders/1wK7MNoIxU3HvxQ6ciA94D8pvvfhT0juW
