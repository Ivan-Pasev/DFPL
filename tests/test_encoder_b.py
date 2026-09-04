import json
import pathlib
import unittest

from tools.independent_encoder_b import (
    encode_bool,
    encode_bytes,
    encode_int_decimal,
    encode_text,
    hex_encode,
    parse_canonical_decimal,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
VECTORS = ROOT / "conformance" / "vectors" / "n0-core-candidate-0001.json"


class EncoderBSentinelTests(unittest.TestCase):
    def test_public_candidate_vector_pack_primitive_bytes(self):
        pack = json.loads(VECTORS.read_text(encoding="utf-8"))
        by_id = {v["vector_id"]: v for v in pack["vectors"]}

        self.assertEqual(
            hex_encode(encode_bool(False)),
            by_id["C3-ENCODE-BOOL-FALSE-0001"]["expected_bytes_hex"],
        )
        self.assertEqual(
            hex_encode(encode_bool(True)),
            by_id["C3-ENCODE-BOOL-TRUE-0001"]["expected_bytes_hex"],
        )
        self.assertEqual(
            hex_encode(encode_bytes(bytes.fromhex(by_id["C3-ENCODE-BYTES-0001"]["input_hex"]))),
            by_id["C3-ENCODE-BYTES-0001"]["expected_bytes_hex"],
        )
        self.assertEqual(
            hex_encode(encode_text(by_id["C3-ENCODE-TEXT-ASCII-0001"]["input"])),
            by_id["C3-ENCODE-TEXT-ASCII-0001"]["expected_bytes_hex"],
        )

    def test_integer_sentinels(self):
        self.assertEqual(hex_encode(encode_int_decimal("0")), "02000000000000000000")
        self.assertEqual(hex_encode(encode_int_decimal("1")), "0200000000000000000101")
        self.assertEqual(hex_encode(encode_int_decimal("-1")), "0201000000000000000101")
        self.assertEqual(
            hex_encode(encode_int_decimal("340282366920938463463374607431768211456")),
            "020000000000000000110100000000000000000000000000000000",
        )

    def test_noncanonical_integer_surface_is_rejected(self):
        for text in ("", "-0", "00", "01", "+1", "1_0", " 1", "1 "):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_canonical_decimal(text)

    def test_nfc_text_collapses_canonically(self):
        precomposed = "é"
        decomposed = "e\u0301"
        self.assertEqual(encode_text(precomposed), encode_text(decomposed))
        self.assertEqual(hex_encode(encode_text(precomposed)), "040000000000000002c3a9")


if __name__ == "__main__":
    unittest.main()
