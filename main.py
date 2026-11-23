#!/usr/bin/env python3
"""Write one six-word story to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The story is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 60 characters, not only white space.
"""

import os
import sys
from pathlib import Path

STORY = "He waited decades. She married another."
# Six words: a lifetime of waiting, undercut in three. The reader
# fills in where he waited, why she left, and whether she knew.

MIN_CHARS = 1
MAX_CHARS = 60
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 60 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"story is {chars} characters, outside 1-60")
    if not text.strip():
        raise ValueError("story is only white space")
    words = text.split()
    if len(words) != 6:
        raise ValueError(f"story is {len(words)} words, not six")
    return chars


def main() -> int:
    try:
        validate(STORY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(STORY, encoding="utf-8")
    print(STORY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
