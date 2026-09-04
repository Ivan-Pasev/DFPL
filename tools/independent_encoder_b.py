"""Independent DFPL N-0 candidate encoder B.

Evidence purpose only. This implementation is intentionally small and derived
from public §8 plus the public candidate registries. It does not import or share
code with DFPL-LAB's Rust encoder. Passing tests establishes only the exercised
candidate sentinel behavior, not N-0 conformance.
"""

from __future__ import annotations

import unicodedata

TAG_BOOL = 0x01
TAG_INT = 0x02
TAG_BYTES = 0x03
TAG_TEXT = 0x04


def _u64_be(n: int) -> bytes:
    if n < 0 or n > 0xFFFFFFFFFFFFFFFF:
        raise ValueError("length out of u64 range")
    return n.to_bytes(8, "big", signed=False)


def encode_bool(value: bool) -> bytes:
    if type(value) is not bool:
        raise TypeError("DFPL Bool requires Python bool")
    return bytes((TAG_BOOL, 0x01 if value else 0x00))


def encode_bytes(value: bytes) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError("DFPL Bytes requires bytes")
    return bytes((TAG_BYTES,)) + _u64_be(len(value)) + value


def normalize_text_nfc(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("DFPL Text requires str")
    return unicodedata.normalize("NFC", value)


def encode_text(value: str) -> bytes:
    normalized = normalize_text_nfc(value)
    payload = normalized.encode("utf-8", "strict")
    return bytes((TAG_TEXT,)) + _u64_be(len(payload)) + payload


def parse_canonical_decimal(text: str) -> int:
    if not isinstance(text, str) or not text:
        raise ValueError("empty integer literal")
    if text == "0":
        return 0
    negative = text.startswith("-")
    digits = text[1:] if negative else text
    if not digits or not digits.isascii() or not digits.isdigit():
        raise ValueError("non-canonical decimal digits")
    if digits.startswith("0"):
        raise ValueError("leading zero or negative zero")
    return -int(digits) if negative else int(digits)


def encode_int_decimal(text: str) -> bytes:
    value = parse_canonical_decimal(text)
    if value == 0:
        return bytes((TAG_INT, 0x00)) + _u64_be(0)
    sign = 0x01 if value < 0 else 0x00
    magnitude_value = abs(value)
    width = (magnitude_value.bit_length() + 7) // 8
    magnitude = magnitude_value.to_bytes(width, "big", signed=False)
    if not magnitude or magnitude[0] == 0:
        raise AssertionError("internal nonminimal magnitude")
    return bytes((TAG_INT, sign)) + _u64_be(len(magnitude)) + magnitude


def hex_encode(data: bytes) -> str:
    return data.hex()
