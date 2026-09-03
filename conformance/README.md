# DFPL Conformance

Conformance is always relative to a Kernel ID, profile, implementation version, and conformance class.

Planned corpus layers:

- parser acceptance/rejection;
- static name/type/phase cases;
- normalization golden vectors;
- canonical value/IR bytes;
- detailed semantic verdict vectors;
- Unicode normalization;
- integer target-range boundaries;
- Set/Map/Record ordering and duplicate rejection;
- malformed evidence/encodings;
- property-based tests;
- parser/canonicalizer fuzzing;
- differential Rust/WASM/JS evaluation;
- metamorphic source transformations;
- replay/domain-separation attacks;
- Decision Certificate tampering;
- target projection adversaries.

The historical four cases—prohibition fires, requirement fails, postcondition fails, all pass—are retained only as a minimum smoke basis, not as complete conformance evidence.
