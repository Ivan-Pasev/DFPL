# Security

DFPL is pre-1.0 and must not yet be treated as a production security boundary.

Security depends on more than semantic evaluation, including:

- evidence construction and verification,
- canonical encoding,
- authorization and capability handling,
- replay/freshness controls,
- Effect Gateway correctness,
- target runtime behavior,
- profile-specific cryptographic assumptions,
- implementation conformance.

Never commit credentials, private keys, access tokens, secrets, or private user data.

Security reports that depend on unreleased private-lab material should be handled outside public issues until an appropriate disclosure path is established.
