#!/usr/bin/env python3
"""Entry point: copy entry.png from this file's directory into the output
directory ($MAKEFUN_OUTPUT_DIR, or /output when unset). Stdlib only.
The copy is byte-identical to the repo's entry.png.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
