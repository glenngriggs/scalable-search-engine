#!/usr/bin/env python3


# """
# Reduce 4: just pass through TF and DF
# Input:  term docID   TF DF
# Output: term docID   TF DF
# """

# import sys
# import itertools

# def keyfunc(line):
#     return line.split()[0]

# def reduce_one_group(term, group):
#     for line in group:
#         print(line.strip())

# def main():
#     for term, group in itertools.groupby(sys.stdin, keyfunc):
#         reduce_one_group(term, group)

# if __name__ == "__main__":
#     main()


"""
Reduce 4: group by docid, compute document norm, re-emit by term.

Input:
    docid term TF IDF

Output:
    term docid TF NORM IDF
"""

import sys
import itertools
import math


def keyfunc(line):
    """Group by docid (before TAB)."""
    return line.partition("\t")[0]


def reduce_one_group(docid_str, group):
    """
    Docid_str: document ID as a string.

    Group: all lines 'docid term TF IDF' for this doc.
    """
    entries = []  # list of (term, TF, IDF)
    sum_sq = 0.0  # this will be the sum of (TF * IDF)^2

    for line in group:
        _, _, value = line.partition("\t")  # 'term TF IDF'
        value = value.strip()
        if not value:
            continue

        parts = value.split()
        if len(parts) != 3:
            continue  # malformed line so we skip

        term, tf_str, idf_str = parts
        tf = int(tf_str)
        idf = float(idf_str)

        weight = tf * idf
        sum_sq += weight * weight  # accumulat the (TF * IDF)^2
        entries.append((term, tf, idf))

    if not entries:
        return

    # norm = sqrt(sum (TF * IDF)^2) for this document
    norm = math.sqrt(sum_sq)

    # Emit one line per term, keyed by term (for next stages)
    # term\tDOCID TF NORM IDF
    for term, tf, idf in entries:
        print(f"{term}\t{docid_str} {tf} {norm} {idf}")


def main():
    """Group by DOCID and reduce."""
    for docid_str, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(docid_str, group)


if __name__ == "__main__":
    main()


# so the job 4 output is: term\tDOCID TF NORM IDF
