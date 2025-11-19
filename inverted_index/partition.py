#!/usr/bin/env -S python3 -u
"""Extract counts from partitioned inverted index segments."""
import sys


for line in sys.stdin:
    key, _, _ = line.partition("\t")
    print(int(key))
