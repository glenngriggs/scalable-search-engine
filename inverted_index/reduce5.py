#!/usr/bin/env python3
"""
Reduce 5: Build final inverted index segments.

Input (grouped by segment):
    segment term IDF docid TF NORM

Output (per segment file):
    term idf docid tf norm docid tf norm ...
"""

import sys
import itertools


def keyfunc(line):
    """Group by segment index (0, 1, or 2)."""
    return line.partition("\t")[0]


def reduce_one_segment(group):
    """segment_key: '0', '1', or '2'."""
    terms = {}

    for line in group:
        _, _, value = line.partition("\t")
        value = value.strip()
        if not value:
            continue

        parts = value.split()
        if len(parts) != 5:
            continue  # malformed

        term, idf_str, docid_str, tf_str, norm_str = parts
        idf = float(idf_str)
        tf = int(tf_str)
        norm = float(norm_str)

        entry = terms.get(term)
        if entry is None:
            # first time seeing this term in the segment
            entry = {"idf": idf, "docs": []}
            terms[term] = entry
        else:
            # Optional sanity check: IDF should be consistent
            # if abs(entry["idf"] - idf) > 1e-6:
            #     continue
            pass

        # remember this posting for the term
        entry["docs"].append((docid_str, tf, norm))

    # Emit final lines: term idf docid tf norm docid tf norm ...
    for term in sorted(terms.keys()):
        entry = terms[term]
        idf = entry["idf"]
        docs = entry["docs"]

        # Sort docids lexicographically (keeps leading zeros)
        docs.sort(key=lambda d: d[0])

        # start with [term, idf]
        fields = [term, str(idf)]

        # append doc triples: DOCID TF NORM
        for docid_str, tf, norm in docs:
            fields.extend([docid_str, str(tf), str(norm)])

        # JOIN everything w/ spaces to match spec format
        print(" ".join(fields))


def main():
    """Group by segment 0/1/2."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_segment(group)


if __name__ == "__main__":
    main()
