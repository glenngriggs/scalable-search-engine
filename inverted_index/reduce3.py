#!/usr/bin/env python3


# """
# Reduce 3: Compute DF per term and attach it to each (term, docID) pair.

# Input lines (grouped by term):
#     term\tdocID1 TF
#     term\tdocID2 TF
#     ...

# Output lines:
#     term docID1\tTF DF
# """

# import sys
# import itertools

# def reduce_one_group(key, group):
#     """
#     key: the term (e.g. "hello")
#     group: all lines like "hello\t034034343 3"
#     """

#     # collect all (docID, TF) pairs for this term
#     doc_tf_list = []
#     for line in group:
#         # line formatting: "term\tdocID TF"
#         _, _, value = line.partition('\t') # value  = "docID TF"
#         value = value.strip()

#         if not value:
#             continue

#         doc_id, tf_str = value.split(" ", 1) # split on first space only
#         doc_tf_list.append((doc_id, tf_str))

#     # document frequency (DF) = # unique documents for this term
#     df = len(doc_tf_list)

#     #emit one line per (term, docID) pair with TF and DF
#     for doc_id, tf_str in doc_tf_list:
#         # output key: "term docID" and value: "TF DF"
#         print(f"{key} {doc_id}\t{tf_str} {df}")

# def keyfunc(line):
#     """return jey term from line."""
#     return line.partition('\t')[0]

# def main():
#     for key, group in itertools.groupby(sys.stdin, keyfunc):
#         reduce_one_group(key, group)

# if __name__ == "__main__":
#     main()


"""
Reduce 3: For each term, compute IDF and emit (docid, term TF IDF).

Input (grouped by term):
    term docid TF

Output:
    docid term TF IDF
"""

import sys
import itertools
import math


def load_total_docs(path="total_document_count.txt"):
    """Read total number of documents as integer."""
    with open(path, encoding="utf-8") as infile:
        text = infile.read().strip()
    return int(text)


def keyfunc(line):
    """Group by term (everything before TAB)."""
    return line.partition("\t")[0]


def reduce_one_group(term, group, total_docs):
    """
    Term: the current term (string).

    Group: all lines "term docid TF."
    """
    postings = []  # list of (docid_str, tf_int)

    for line in group:
        _, _, value = line.partition("\t")  # value = "docid TF"
        value = value.strip()
        if not value:
            continue

        # split "DOCID TF"
        docid_str, tf_str = value.split()
        postings.append((docid_str, int(tf_str)))

    if not postings:
        return

    # DF = # of documents that contain this term
    df = len(postings)

    # IDF = log10(N / DF), where N is the total # of docs
    idf = math.log10(total_docs / df)

    # Emit one line per document containig this term: docid\tterm TF IDF
    for docid_str, tf in postings:
        print(f"{docid_str}\t{term} {tf} {idf}")


def main():
    """Read lines from stdin and emit (docid, 'term TF IDF')."""
    total_docs = load_total_docs()  # N
    for term, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(term, group, total_docs)


if __name__ == "__main__":
    main()


# IDEA:
    # job 3 output is : DOCID\tterm TF IDF
    # each line: one term in document, with its TF and IDF
