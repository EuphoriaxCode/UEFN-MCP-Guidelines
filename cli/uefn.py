#!/usr/bin/env python3
"""Entry point: python cli/uefn.py <command> ...  (or cli/uefn.cmd on Windows)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uefncli.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
