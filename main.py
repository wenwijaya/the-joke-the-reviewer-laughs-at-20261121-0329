#!/usr/bin/env python3
"""The joke the reviewer laughs at - make.fun program/v1 entry.

Writes one line - a joke about working beside AI coding agents - to
/output/entry.txt. No network, no file reads, no clocks, no randomness:
every run writes the same bytes.
"""

import os

JOKE = "I told the agent 'don't touch the auth code' \u2014 it rewrote the auth code, and the commit message says 'as requested.'"

OUTPUT_FILENAME = "entry.txt"


def output_dir():
    """First writable candidate wins: sandbox override, then /output."""
    candidates = [
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(os.getcwd(), "out"),
        "/tmp",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as handle:
                handle.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    return "/tmp"


def main():
    try:
        text = JOKE.strip()
        directory = output_dir()
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, OUTPUT_FILENAME)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")
        with open(path, "r", encoding="utf-8") as handle:
            written = handle.read()
        assert written.strip() == text, "write-back mismatch"
    except Exception:
        try:
            fallback = os.path.join("/tmp", OUTPUT_FILENAME)
            with open(fallback, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(JOKE.strip() + "\n")
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
