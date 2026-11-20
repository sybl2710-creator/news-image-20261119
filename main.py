"""MakeFun entrypoint: publish the rendered front page as entry.png."""

import os
import shutil

SOURCE = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE)
    if not os.path.isfile(src):
        raise SystemExit(f"missing source image: {src}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        dest = os.path.join(out_dir, SOURCE)
        os.makedirs(out_dir, exist_ok=True)
    else:
        dest = os.path.join("/output", SOURCE)
        os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, dest)


if __name__ == "__main__":
    main()
