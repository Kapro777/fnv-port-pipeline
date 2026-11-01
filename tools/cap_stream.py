#!/usr/bin/env python3
"""Consume stdin completely while writing only a bounded prefix to a file."""

import sys


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} OUTPUT LIMIT", file=sys.stderr)
        return 2

    output = sys.argv[1]
    limit = int(sys.argv[2])
    written = 0
    truncated = False

    with open(output, "wb") as dst:
        while True:
            chunk = sys.stdin.buffer.read(65536)
            if not chunk:
                break
            if written < limit:
                part = chunk[: limit - written]
                dst.write(part)
                written += len(part)
                if written >= limit:
                    truncated = True

        if truncated:
            dst.write(b"\n[DesertDroid] diagnostico truncado em 64 MiB\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
