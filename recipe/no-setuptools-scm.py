"""Avoid circular dependency on ``setuptools-scm``."""

import sys
import os
import re
import difflib

from pathlib import Path

UTF8 = {"encoding": "utf-8"}
SRC_DIR = Path(os.environ["SRC_DIR"])
PKG_VERSION = os.environ["PKG_VERSION"]
PYPROJECT = SRC_DIR / "pyproject.toml"


def main() -> int:
    old_text = PYPROJECT.read_text(**UTF8)
    new_text = old_text.replace('dynamic = ["version"]', f'version = "{PKG_VERSION}"')
    new_text = re.sub(r'"setuptools[_\-]scm.*?",?', "", new_text)
    diff = difflib.unified_diff(
        old_text.splitlines(), new_text.splitlines(), "BEFORE", "AFTER"
    )
    print("\n".join(diff))
    PYPROJECT.write_text(new_text, **UTF8)


if __name__ == "__main__":
    sys.exit(main())
