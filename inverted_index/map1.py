#!/usr/bin/env python3
"""Map 1."""

import sys
import bs4

# Parse one HTML document at a time.

HTML = ""   # accumulate one full HTML file here
for line in sys.stdin:
    # Assuming well-formed HTML docs:
    # - Starts with <!DOCTYPE html>
    # - End with </html>
    # - Contains a trailing newline
    if "<!DOCTYPE html>" in line:
        # new document starts -> reset buffer to this line
        HTML = line
    else:
        # still in the same doc --> append line
        HTML += line

    # If we're at the end of a document, keep reading
    if "</html>" not in line:
        continue

    # -------at this point we have a complete HTML doc in HTML ------- #

    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(HTML, "html.parser")

    # Get docid from document
    # <meta eecs485_docid="00035015">
    doc_id = soup.find("meta",
                       attrs={"eecs485_docid": True}).get("eecs485_docid")

    # Parse content from document
    # get_text() will strip extra whitespace and
    # concatenate content, separated by spaces
    element = soup.find("html")  # root <html> tag

    content = element.get_text(separator=" ", strip=True)

    # Remove extra newlines
    content = content.replace("\n", " ")

    # emit one line per doc
    # key = docID
    # value = full plain text content
    # FIXME Map 1 output.  Emit one line for each document, including the doc
    # ID and document content (You will need them later!)
    print(f"{doc_id}\t{content}")
