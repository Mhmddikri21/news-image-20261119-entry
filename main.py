#!/usr/bin/env python3
"""news-image-20261119 entry: validate the bundled broadsheet PNG
and publish it to /output/entry.png.

The image itself (entry.png, next to this file) is the entry: a
1024x1024 broadsheet summing up Thursday 19 November 2026 in 55
stories — the Trump-Xi-Putin trilateral in Shenzhen, the ICJ's
Myanmar genocide ruling, the third Kerch Bridge strike, the Houthi
missile on Riyadh's PIF Tower, GTA VI's launch day, the Dow's
1,101-point drop, Anthropic's record IPO, and 48 more, with a UTC
timeline, a numbers strip, a world map and a DATE CHECK box for
stories that broke before the day.

This program does no drawing and no network. It reads entry.png,
checks it is a whole, well-formed PNG (signature, chunk CRCs,
1024x1024 IHDR, IEND present), and copies the exact bytes to
/output/entry.png. Run it twice and the output is byte-identical,
because the input never changes and nothing here depends on time,
randomness or the environment.
"""
import binascii
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = "/output/entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def walk_chunks(data):
    """Yield (type, payload) for every chunk, verifying each CRC."""
    if data[:8] != PNG_SIGNATURE:
        fail("not a PNG file (bad signature)")
    pos = 8
    seen = []
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail(f"truncated chunk {kind!r}")
        payload = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(">I", data[pos + 8 + length:end])[0]
        actual_crc = binascii.crc32(kind + payload) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail(f"bad CRC in chunk {kind!r}")
        seen.append((kind, payload))
        pos = end
        if kind == b"IEND":
            break
    if pos != len(data):
        fail("trailing bytes after IEND")
    return seen


def check_image(data):
    if len(data) > 1048576:
        fail(f"image is {len(data)} bytes, over the 1 MiB limit")
    chunks = walk_chunks(data)
    kinds = [kind for kind, _ in chunks]
    if not kinds or kinds[0] != b"IHDR":
        fail("first chunk is not IHDR")
    if kinds[-1] != b"IEND":
        fail("last chunk is not IEND")
    if b"IDAT" not in kinds:
        fail("no IDAT chunk")
    ihdr = chunks[0][1]
    width, height, depth, colour = struct.unpack(">IIBB", ihdr[:10])
    if (width, height) != (1024, 1024):
        fail(f"expected 1024x1024, got {width}x{height}")
    if depth != 8 or colour != 2:
        fail(f"expected 8-bit truecolour, got depth {depth} colour {colour}")
    return len(chunks)


def main():
    with open(SOURCE, "rb") as handle:
        data = handle.read()
    chunk_count = check_image(data)
    digest = hashlib.sha256(data).hexdigest()
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    with open(TARGET, "wb") as handle:
        handle.write(data)
    with open(TARGET, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("output differs from source")
    print(f"wrote {TARGET} {len(data)} bytes "
          f"sha256={digest} chunks={chunk_count}")


if __name__ == "__main__":
    main()
