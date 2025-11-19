#!/usr/bin/env python3
"""Reduce 0."""

import sys
import itertools


# def reduce_one_group(key, group):
def reduce_one_group(group):
    """Sum all the values for this key (count)."""
    total = 0
    for line in group:
        # Line format: "count\t1"
        _, _, value = line.partition('\t')  # _ <- count ; _ <- \t ; value <- 1
        total += int(value)
    print(total)


def keyfunc(line):
    """Extract the key (before tab)."""
    return line.partition('\t')[0]


def main():
    """Hadoop Streaming guarantees exactly one group."""
    #     reduce_one_group(key, group)
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
