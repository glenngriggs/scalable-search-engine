#!/usr/bin/env python3
"""Reduce 1."""

import sys

# identity reducer - just pass mapper output to stdout unchanged
for line in sys.stdin:
    # line already looks like: docid \t content
    print(line, end='')  # keep original newline
