#!/usr/bin/env python3
"""Copy entry.png to the make.fun output directory.

Standard library only. No drawing happens here; the image is built
by draw_news.py at build time.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, 'entry.png')
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, 'entry.png'))


if __name__ == '__main__':
    main()
