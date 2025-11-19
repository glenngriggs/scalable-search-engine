"""index/api/__init__.py from flask import current_app."""
from pathlib import Path  # noqa: E402 pylint: disable=wrong-import-position
from index import app  # noqa: E402 pylint: disable=wrong-import-position

# Globals to hold your loaded data
INVERTED_INDEX = {}
STOPWORDS = set()
PAGERANK = {}


def register_blueprints(flask_app):
    """Register API blueprints with the Flask app."""
    flask_app.register_blueprint(bp)


def load_index():
    """Load into memory."""
    index_path = Path(app.config["INDEX_PATH"])
    base_dir = index_path.parent.parent
    stopwords_path = base_dir / "stopwords.txt"
    pagerank_path = base_dir / "pagerank.out"

    STOPWORDS.clear()
    with open(stopwords_path, "r", encoding="utf-8") as f:
        for line in f:
            STOPWORDS.add(line.strip())

    PAGERANK.clear()
    with open(pagerank_path, "r", encoding="utf-8") as f:
        for line in f:
            doc_id, rank = line.split(",")
            PAGERANK[doc_id] = float(rank)

    INVERTED_INDEX.clear()
    with open(index_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            term = parts[0]
            idf = float(parts[1])

            postings = {}
            # fields: docid tf norm in groups of 3
            for i in range(2, len(parts), 3):
                doc_id = parts[i]
                tf = int(parts[i + 1])
                doc_len = float(parts[i + 2])
                postings[doc_id] = {
                    "tf": tf,
                    "doc_len": doc_len,
                }

            INVERTED_INDEX[term] = {
                "idf": idf,
                "docs": postings,
            }


from .main import bp  # noqa: E402 pylint: disable=wrong-import-position
