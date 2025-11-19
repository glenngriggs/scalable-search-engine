#!/usr/bin/env python3

"""Map 2: (docid, raw text) -> (term docid, 1) with cleaning + stopwords."""

import sys
import re

# Load stopwords once at startup
STOPWORDS = set()
with open("stopwords.txt", encoding="utf-8") as infile:
    for line in infile:
        word = line.strip()  # remove whitespace/NL
        if word:  # skip emty lines
            STOPWORDS.add(word)  # add a stopword to the set


def tokenize_and_filter(text):
    """Clean text, split into tokens, drop stopwords."""
    # Remove non-alphanumeric characters (but keep spaces)
    # everything except letters, digits, and spaces becomes ""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)

    # make it case-insensitive
    text = text.casefold()

    # split into whitespace-delimited tokens
    tokens = text.split()

    # Drop stopwords and empty tokens
    # return tokens that are not empty + not stopwords
    return [tok for tok in tokens if tok and tok not in STOPWORDS]


def main():
    """
    Read (docid, content) lines from stdin and.

    Emit (term docid, 1) pairs.
    """
    # note --> each line from stdin: "docid\tcontent"
    for line in sys.stdin:
        line = line.rstrip("\n")  # strip trailing newline
        if not line:    # skip empty lines
            continue

        # split at the first tab : doc_id, "\t", content
        doc_id, _, content = line.partition("\t")
        if not doc_id:
            # malformed input so skip
            continue

        # clean + tokenize the content
        terms = tokenize_and_filter(content)

        # Emit one (term docid) pair per occurence with count 1
        # kwy : "term DOCID"
        # value: "1"
        for term in terms:
            print(f"{term} {doc_id}\t1")


if __name__ == "__main__":
    main()


# """Map 2: Extract terms and emit (term, docID) pairs w/ count 1.."""

# import sys


# # loop through each line provided to mapper
# for line in sys.stdin: # line comes from job 1 reducer: XXXXX/thello world..
#     line = line.strip() # remove newlines and leading/trailing spaces

#     # skip empty lines
#     if not line:
#         continue

#     # split line into docID and content (i.e. full text)
#         # line format: "docID\tcontent"
#     doc_id, _, content = line.partition('\t')
# doc_id <- XXXXX ; _ <- \t ; content <- hello world..

#     # split content into individual terms
#     terms = content.split() # terms = [hello, world..]

#     # emit (term, docID) pairs --> 1 for term frequency counting
#     for term in terms:
#         print(f"{term} {doc_id}\t1")  # key = term ; value = docID\t1
