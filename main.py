#!/usr/bin/env python3
"""One Emoji, One Dream Vacation.

Writes exactly one emoji -- the sunrise over the sea -- to entry.txt.

The pick: U+1F305 SUNRISE OVER THE SEA. A dream vacation is not a place
on a map, it is the first morning of the trip: you wake before anyone
else, walk down to the water, and watch the sun come up over an ocean
you do not have to leave. One picture, no words -- a postcard a stranger
can read at a glance, in any country, on any screen.
"""

import os
import sys
import unicodedata

# U+1F305 SUNRISE OVER THE SEA -- dawn breaking over the water,
# the first morning of a dream trip.
EMOJI = "\U0001F305"

# The gate (from the competition rules): /output/entry.txt must be
# UTF-8 text of 1 to 8 characters, not only white space.
MAX_CHARS = 8


def is_emoji(char):
    """Best-effort stdlib check that a single character is an emoji.

    Covers the pictograph blocks the Unicode data file knows about:
    So (Symbol, other) and Sk (Symbol, modifier) cover the emoji
    pictographs, and the dedicated emoji presentation ranges.
    """
    code = ord(char)
    if 0x1F300 <= code <= 0x1FAFF:  # Misc Symbols & Pictographs, Emoticons,
        return True                # Transport & Map, Supplemental Symbols
    if 0x2600 <= code <= 0x27BF:   # Misc Symbols / Dingbats
        return True
    if 0x2190 <= code <= 0x21FF:   # Arrows (some are emoji)
        return True
    if 0x2300 <= code <= 0x23FF:   # Misc Technical (some are emoji)
        return True
    category = unicodedata.category(char)
    return category in ("So", "Sk")


def validate(text):
    """Enforce the one-emoji rule before anything is written."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1 to 8 characters, got %d" % len(text)
        )
    if text.strip() == "":
        raise ValueError("entry must not be only white space")
    if len(text) != 1:
        raise ValueError(
            "entry must be exactly one emoji, got %d characters" % len(text)
        )
    if not is_emoji(text):
        raise ValueError("entry must be exactly one emoji, got %r" % text)
    return text


def main():
    entry = validate(EMOJI)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(entry)
    # Round-trip guard: what is on disk must be exactly the one emoji,
    # byte for byte -- a partial write or an encoding slip must fail
    # loudly here, not silently reach the gate as an invalid entry.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != entry:
        raise ValueError(
            "entry.txt on disk %r does not match the entry %r"
            % (written, entry)
        )
    validate(written)
    print(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
