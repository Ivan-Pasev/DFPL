# Ω-DFPL §8 — Canonical Encoding and IDs

**Status:** normative draft / freeze candidate

## 8.0 Purpose

Canonical encoding maps normalized DFPL semantic objects to one exact byte sequence independent of host language, runtime, platform, locale, insertion order, memory layout, or serializer defaults.

```text
Encode_K : CanonicalObject -> Bytes
```

Content identities are derived only from canonical bytes under explicit domain separation.

```text
ObjectID = H(domain_sep || canonical_bytes)
```

This section freezes the abstract byte model and identity construction. A Kernel version MUST pin the exact tag registry, integer representation, text policy, collection rules, digest algorithm, and domain-separation constants it uses.

## 8.1 Encoding invariants

For every object in the supported canonical domain:

1. encoding is deterministic;
2. the encoding is self-delimiting or length-delimited at every variable-width boundary;
3. distinct type tags cannot collide;
4. encoding does not depend on host insertion order;
5. noncanonical inputs are rejected rather than repaired silently;
6. decoding, where defined, either returns the unique corresponding canonical object or rejects;
7. canonical IDs exclude the field that stores the ID being computed.

## 8.2 Byte model

The canonical byte alphabet is the octet set `0x00..0xFF`.

All multi-byte unsigned lengths use big-endian unsigned magnitude. Fixed-width tag fields and length prefixes are defined by the Kernel Descriptor.

N-0 candidate primitives:

```text
TAG        : u8
LEN        : u64 big-endian
BYTES[n]   : raw octets
```

A future Kernel MAY change widths only by changing Kernel identity/version.

## 8.3 Domain separation

Every content-ID family uses a distinct ASCII/UTF-8 domain-separation literal terminated by `0x00`.

Candidate N-0 literals:

```text
DFPL-KERNEL-v1\0
DFPL-TYPE-v1\0
DFPL-LAW-v1\0
DFPL-PLAN-v1\0
DFPL-CAP-v1\0
DFPL-AUTH-v1\0
DFPL-DECISION-v1\0
DFPL-RECEIPT-v1\0
DFPL-CHECKPOINT-v1\0
```

Equal canonical bytes under different object families therefore do not intentionally share IDs.

## 8.4 Hash algorithm

N-0 selects SHA-256 as the baseline content-ID digest for Kernel/Law and cross-artifact identity unless an explicitly versioned profile specifies another algorithm.

This is a portability choice, not a claim that SHA-256 proves semantic correctness.

```text
ID = SHA256(domain_sep || canonical_bytes)
```

The digest is rendered externally as lowercase hexadecimal when a text representation is needed. Hex rendering is not itself the hashed content.

## 8.5 Primitive tags

Every value and structural node begins with a Kernel-pinned type/node tag.

Candidate semantic tag families include:

```text
BOOL
INT
BYTES
TEXT
DIGEST
ADDRESS
OPTION_NONE
OPTION_SOME
LIST
SET
MAP
RECORD
REF
LOCAL_REF
IF
LET
NOT
AND
OR
ADD
SUB
NEG
MUL
EQ
NE
LT
LE
GT
GE
CLAUSE
LAW_IR
TYPE_DESC
```

The final numeric tag registry is part of the Kernel Descriptor and MUST be collision-free.

## 8.6 Boolean encoding

```text
false = TAG_BOOL || 0x00
true  = TAG_BOOL || 0x01
```

Any other Boolean payload is invalid.

## 8.7 Integer encoding

DFPL `Int` is arbitrary precision. Canonical encoding MUST therefore not use a fixed host machine width.

N-0 uses sign-plus-minimal-magnitude encoding:

```text
TAG_INT || SIGN || LEN || MAGNITUDE
```

where:

- `SIGN = 0x00` for zero/nonnegative;
- `SIGN = 0x01` for negative;
- `MAGNITUDE` is the minimal big-endian unsigned absolute value;
- zero has `LEN=0` and empty magnitude;
- leading zero magnitude octets are forbidden;
- negative zero is forbidden.

Thus each mathematical integer has exactly one encoding.

## 8.8 Bytes encoding

```text
TAG_BYTES || LEN || raw_bytes
```

Length is measured in octets.

## 8.9 Text encoding

Text is first normalized by the exact Unicode version and normalization policy pinned by the Kernel Descriptor, then encoded as UTF-8.

```text
TAG_TEXT || LEN || utf8_bytes
```

Invalid UTF-8 and noncanonical Unicode normalization are rejected.

No locale-dependent case folding, transliteration, or collation occurs.

## 8.10 Digest and Address

Digest:

```text
TAG_DIGEST || Encode(algorithm_id) || LEN || digest_bytes
```

Address:

```text
TAG_ADDRESS || Encode(domain_id) || LEN || address_bytes
```

Algorithm/domain identity is part of the semantic bytes. Equal payload bytes under different algorithms/domains are distinct values.

## 8.11 Option

```text
None<T> = TAG_OPTION_NONE || EncodeType(T)
Some(v) = TAG_OPTION_SOME || EncodeType(type(v)) || Encode(v)
```

Typed absence is therefore unambiguous.

## 8.12 List

```text
TAG_LIST || EncodeType(T) || LEN_COUNT || Encode(v1) ... Encode(vn)
```

Element order is semantic and preserved.

## 8.13 Set

Set elements are already normalized/sorted by `CanonicalOrder_K` in §5.

```text
TAG_SET || EncodeType(K) || LEN_COUNT || Encode(v1) ... Encode(vn)
```

The encoder verifies strict canonical order and no duplicates. It MUST NOT sort/repair malformed supposedly canonical IR silently.

## 8.14 Map

Map entries are already sorted by canonical key order.

```text
TAG_MAP || EncodeType(K) || EncodeType(V) || LEN_COUNT ||
  Encode(k1)||Encode(v1) ... Encode(kn)||Encode(vn)
```

Duplicate/non-increasing canonical keys are invalid.

## 8.15 Record

```text
TAG_RECORD || LEN_FIELDS ||
  EncodeFieldId(f1)||Encode(v1) ... EncodeFieldId(fn)||Encode(vn)
```

Fields MUST be in strict canonical field order. Field IDs are normalized Text identifiers or Kernel-defined structural IDs encoded canonically.

## 8.16 Type descriptors

Every normalized type descriptor has a canonical structural encoding.

Primitive type descriptors use fixed tags; parameterized/container/record types recursively encode their normalized parameters/fields.

Type aliases never appear in canonical bytes.

Candidate:

```text
TypeID_K(T) = SHA256("DFPL-TYPE-v1\0" || KernelID || EncodeType(T))
```

Whether `TypeID` remains a public first-class artifact is a profile/API choice; canonical type bytes remain normative.

## 8.17 Ref and LocalRef

Resolved state/evidence reference:

```text
TAG_REF || phase_tag || EncodeType(T) || LEN_PATH || EncodeFieldId(p1)...EncodeFieldId(pn)
```

Lexical reference:

```text
TAG_LOCAL_REF || EncodeType(T) || U64(depth) || U64(slot)
```

Source binder names do not appear, preserving alpha invariance.

## 8.18 Expressions

Each expression constructor is encoded as:

```text
NODE_TAG || node-specific typed payload || recursively encoded children
```

Children are encoded in the normative semantic order from the canonical expression tree. No encoder algebraic optimization/reordering is permitted.

For example:

```text
And(a,b) = TAG_AND || Encode(a) || Encode(b)
If(c,t,f) = TAG_IF || Encode(c) || Encode(t) || Encode(f)
```

## 8.19 Clauses

```text
TAG_CLAUSE || EncodeText(clause_id) || Encode(predicate)
```

The clause class is supplied structurally by the containing LawIR field, not duplicated unless the Kernel tag registry explicitly includes it.

## 8.20 LawIRBody encoding

LawIRBody encodes normalized context schemas followed by the six clause collections in fixed class order:

1. pre invariants;
2. prohibitions;
3. requirements;
4. postconditions;
5. post invariants;
6. transition invariants.

Each collection is count-delimited and its clauses are already in strict canonical ClauseID order.

Conceptually:

```text
TAG_LAW_IR ||
  EncodeSchema(pre) ||
  EncodeSchema(post) ||
  EncodeSchema(evidence) ||
  EncodeClauseList(pre_inv) ||
  EncodeClauseList(forbid) ||
  EncodeClauseList(require) ||
  EncodeClauseList(postcond) ||
  EncodeClauseList(post_inv) ||
  EncodeClauseList(trans_inv)
```

## 8.21 Kernel Descriptor

A Kernel Descriptor is the exact normative identity manifest for one kernel version. It binds at least:

```text
KernelDescriptor {
  kernel_semver_or_version_label
  grammar_profile
  type_system_profile
  normalization_profile
  law_ir_profile
  encoding_profile
  dynamic_semantics_profile
  decision_algebra_profile
  unicode_version
  unicode_normalization
  tag_registry_version
  hash_algorithm
  domain_separation_registry
}
```

The descriptor MUST reference immutable normative artifacts/content or embed equivalent immutable profile identifiers.

## 8.22 KernelID

```text
KernelID = SHA256(
  "DFPL-KERNEL-v1\0" || EncodeKernelDescriptor(KernelDescriptor)
)
```

A change that alters normative grammar, typing, normalization, canonical IR, encoding, dynamic semantics, decision algebra, Unicode policy, tag registry, or domain separation requires a different Kernel Descriptor and therefore a different KernelID.

Different KernelIDs do not automatically imply behavioral incompatibility; compatibility is a separate explicit relation.

## 8.23 LawID

```text
LawID = SHA256(
  "DFPL-LAW-v1\0" || KernelID || EncodeLawIRBody(LawIRBody)
)
```

`law_id` itself is not in `LawIRBody` and cannot self-participate in the hash.

Changing excluded provenance/comments/source layout does not alter LawID; changing canonical semantic content does.

## 8.24 Other system IDs

The same pattern applies to system artifacts, with their own bodies and domain separators:

```text
PlanID
CapabilityID
AuthorizationID
DecisionID
ReceiptID
CheckpointID
```

Each profile/spec MUST define the exact body being encoded and MUST exclude the identity field being computed.

## 8.25 Canonical decoder

A conformant decoder, where provided, MUST reject:

- unknown tags under the active Kernel;
- truncated input;
- trailing bytes when decoding a single exact object;
- nonminimal integer magnitudes;
- negative zero;
- invalid UTF-8;
- noncanonical Unicode text;
- duplicate/unsorted Set or Map entries;
- unsorted/duplicate Record fields;
- unsorted/duplicate ClauseIDs;
- length overrun/underflow;
- structurally invalid type/expression nodes.

It MUST NOT accept multiple byte representations for the same canonical object.

## 8.26 Golden vectors

§8 requires machine-readable golden vectors containing at least:

```text
vector_id
kernel_descriptor
object_kind
canonical_object_fixture
expected_hex_bytes
expected_sha256_id?
status
```

Initial mandatory classes:

1. Bool false/true;
2. Int 0, 1, -1, boundary-size large magnitudes;
3. empty/nonempty Bytes;
4. normalized Text including multi-byte Unicode;
5. Option None/Some;
6. List/Set/Map/Record;
7. Ref/LocalRef;
8. representative expression trees;
9. one complete LawIRBody;
10. malformed/noncanonical rejection cases.

Golden hash vectors MUST NOT be published as normative until the exact Kernel Descriptor/tag registry/domain constants are frozen and independently reproduced.

## 8.27 Implementation independence

Rust, JavaScript, WASM, Python, Solidity, Tcl, Wolfram, or any serializer/library is conformant only if it reproduces the canonical bytes exactly over its declared supported domain.

JSON, CBOR, MessagePack, protobuf, bincode, SCALE, RLP, SSZ, ASN.1, or another library MAY be used as an internal implementation technique only if its output is proven/validated to equal the DFPL canonical encoding. None is semantic authority merely by being widely used.

## 8.28 Security limits

Content addressing provides identity/binding under the selected hash assumptions. It does not establish:

- authorship;
- authentication;
- authorization;
- semantic correctness;
- proof of execution;
- legal validity.

`Hash != Proof` remains normative.

## 8.29 Theorem/property targets

- **T-ENC-01 Determinism**: equal canonical objects produce equal bytes.
- **T-ENC-02 Prefix/unambiguous framing**: structured decoding is unique for valid encoded objects.
- **T-ENC-03 Type-tag separation**: distinct tagged semantic types cannot encode identically solely through payload coincidence.
- **T-ENC-04 Integer uniqueness**: each mathematical Int has one canonical encoding.
- **T-ENC-05 Collection-order preservation**: successful encoding requires the §5 canonical structural order.
- **T-ENC-06 Decode round-trip**: `Decode_K(Encode_K(x)) = x` for supported canonical objects.
- **T-ENC-07 Noncanonical rejection**: alternate encodings for canonical-equivalent values are rejected.
- **T-ENC-08 LawID stability**: equal KernelID + equal LawIRBody yields equal LawID.
- **T-ENC-09 Metadata non-interference**: excluded metadata cannot alter LawID.
- **T-ENC-10 Kernel sensitivity**: a normative Kernel Descriptor change changes the descriptor bytes and, subject to hash assumptions, KernelID.

These are obligations, not mechanically proved claims.

## 8.30 Freeze consequence

DFPL-K now has a candidate exact path:

```text
Source
 -> Typed AST
 -> Canonical Law IR
 -> Deterministic Verdict
 -> Canonical Bytes
 -> KernelID/LawID
```

**NEXT:** §9 Decision Certificates — canonical certificate body, binding to KernelID/LawID/pre/post/evidence commitments/Verdict, evaluator/proof profile, replay/freshness context, certificate identity, and verification rules.
