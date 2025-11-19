#!/usr/bin/env python3
"""Map 3: Group by term to prepare for document frequency (DF) calculation.."""

import sys

# loop through each line provided to mapper
for line in sys.stdin:
    line = line.strip()  # strip whitespace and newlines

    # skip empty lines
    if not line:
        continue

    # split into "term docID" and "TF"
    key_part, _, tf_str = line.partition('\t')
    # key_part <- term docID ; _ <- \t ; tf_str <- TF

    term, doc_id = key_part.split(" ", 1)
    # split params. mean split on first space only
    # and return 2 parts (before, after)

    # mapper output: key = term ; value = "docID TF"
    print(f"{term}\t{doc_id} {tf_str}")
