#!/usr/bin/env python3
"""Map 4: identity mapper for (docid, 'term TF IDF')."""

import sys


def main():
    """Read (docid, 'term TF IDF') lines from stdin and emit them as is."""
    for line in sys.stdin:
        if not line:
            continue
        # Just forward the line  as it is
        sys.stdout.write(line)


if __name__ == "__main__":
    main()


# so the data stays: DOCID\tterm TF IDF
