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
    def _vectors(self):
        pack = json.loads(VECTORS.read_text(encoding="utf-8"))
        return {v["vector_id"]: v for v in pack["vectors"]}

    def test_public_candidate_vector_pack_primitive_bytes(self):
        by_id = self._vectors()
        actual = {
            "C3-ENCODE-BOOL-FALSE-0001": hex_encode(encode_bool(False)),
            "C3-ENCODE-BOOL-TRUE-0001": hex_encode(encode_bool(True)),
            "C3-ENCODE-BYTES-0001": hex_encode(
                encode_bytes(bytes.fromhex(by_id["C3-ENCODE-BYTES-0001"]["input_hex"]))
            ),
            "C3-ENCODE-TEXT-ASCII-0001": hex_encode(
                encode_text(by_id["C3-ENCODE-TEXT-ASCII-0001"]["input"])
            ),
        }
        for vector_id, actual_hex in actual.items():
            print(f"DFPL_SENTINEL_B {vector_id} {actual_hex}")
            self.assertEqual(actual_hex, by_id[vector_id]["expected_bytes_hex"])

    def test_integer_sentinels(self):
        by_id = self._vectors()
        for vector_id in (
            "C3-ENCODE-INT-ZERO-0001",
            "C3-ENCODE-INT-POS-ONE-0001",
            "C3-ENCODE-INT-NEG-ONE-0001",
            "C3-ENCODE-INT-2POW128-0001",
        ):
            vector = by_id[vector_id]
            actual_hex = hex_encode(encode_int_decimal(vector["input_decimal"]))
            print(f"DFPL_SENTINEL_B {vector_id} {actual_hex}")
            self.assertEqual(actual_hex, vector["expected_bytes_hex"])

    def test_noncanonical_integer_surface_is_rejected(self):
        for text in ("", "-0", "00", "01", "+1", "1_0", " 1", "1 "):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_canonical_decimal(text)

    def test_nfc_text_collapses_canonically(self):
        by_id = self._vectors()
        vector = by_id["C3-ENCODE-TEXT-NFC-0001"]
        precomposed = vector["input"]
        decomposed = vector["equivalent_input"]
        self.assertEqual(encode_text(precomposed), encode_text(decomposed))
        actual_hex = hex_encode(encode_text(precomposed))
        print(f"DFPL_SENTINEL_B C3-ENCODE-TEXT-NFC-0001 {actual_hex}")
        self.assertEqual(actual_hex, vector["expected_bytes_hex"])


if __name__ == "__main__":
    unittest.main()
