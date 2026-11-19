#!/usr/bin/env python3
"""Place the drawn front page where the grader reads it.

The entry image is rendered ahead of time by gen.py and shipped in
this repository as entry.png; this program only puts a byte-identical
copy at the output path. Standard library only, no network, no input
besides the bundled image file.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(target_dir, "entry.png"))


if __name__ == "__main__":
    main()
