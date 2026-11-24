#!/usr/bin/env python3
"""make.fun entry point for `news-image-20261124`.

Writes the world-news poster to the output directory: copies the committed
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, or to `/output/entry.png` when
the harness does not set that environment variable.

Standard library only. No network, no randomness, no timestamps: the same
committed image is always copied, byte for byte.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    try:
        os.chmod(dst, 0o644)
    except OSError:
        pass
    print("wrote {}".format(dst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
