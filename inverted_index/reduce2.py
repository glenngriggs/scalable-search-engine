#!/usr/bin/env python3
"""Reduce 2: Sum counts to compute term frequency (TF).."""

import sys
import itertools


def reduce_one_group(key, group):
    """
    Key: "term docID".

    Group: all lines like "term docID."
    """
    total = 0
    for line in group:
        # Line format: "term DOCID\t1"
        _, _, value = line.partition('\t')  # _ <- count ; _ <- \t ; value <- 1
        total += int(value)

    # output format: "term docID\tTF"
    print(f"{key}\t{total}")


def keyfunc(line):
    """Extract the key (before tab)."""
    return line.partition('\t')[0]


def main():
    """
    Itertools.groupby reequires input sorted by key.

    Madoop does the sort for us before calling reduceer.
    """
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()


# IDEA:
    # job 2 output is : term DOCID\tTF
