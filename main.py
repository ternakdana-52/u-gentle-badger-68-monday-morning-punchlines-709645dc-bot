"""Monday Morning Punchlines — make.fun entry.

Writes one joke about Monday mornings to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set). Deterministic,
no network, no randomness.
"""

import os
import sys

JOKE = "Monday is the only day that shows up to work before I do, and it has the nerve to act surprised that I am late."


def main() -> int:
    line = JOKE
    if not 1 <= len(line) <= 200:
        print(f"invalid length: {len(line)} chars (must be 1-200)", file=sys.stderr)
        return 1
    if not line.strip():
        print("invalid: line is only whitespace", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("invalid: line must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 32 for ch in line):
        print("invalid: line contains control characters", file=sys.stderr)
        return 1
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"invalid: line is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    # Read back and verify the written file matches exactly.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        print("verification failed: written file differs from the line", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(line)} chars, verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
