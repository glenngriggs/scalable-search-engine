#!/usr/bin/env python3
"""
Map 5: Assign each (term, docid) posting to a segment by docid % 3.

Input:
    term docid TF NORM IDF

Output:
    segment term IDF docid TF NORM
"""

import sys


def main():
    """Read (term, 'docid TF NORM IDF') lines from stdin and."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # split into term and the rest
        term, _, value = line.partition("\t")
        parts = value.split()

        # expect: DOCID TF NORM ID --> these 4 pieces
        if len(parts) != 4:
            continue  # malformed line

        docid_str, tf_str, norm_str, idf_str = parts

        # Segment by docid % 3 --> segemnt index is: 0, 1, 2
        seg = int(docid_str) % 3

        # Mapper output:
        # Key: segment
        # value: "term IDF docid TF NORM"
        print(f"{seg}\t{term} {idf_str} {docid_str} {tf_str} {norm_str}")


if __name__ == "__main__":
    main()
