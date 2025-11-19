"""Index/api/main.py."""

import math
import re
from collections import Counter
from index.api import INVERTED_INDEX, STOPWORDS, PAGERANK
# from pathlib import Path
# import index
from flask import Blueprint, jsonify, request


CLEAN_RE = re.compile(r"[^a-zA-Z0-9 ]+")

bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route("/", methods=["GET"])
def api_root():
    """Return a list of services available."""
    return jsonify({
        "hits": "/api/v1/hits/",
        "url": "/api/v1/",
    })


@bp.route("/hits/", methods=["GET"])
def api_hits():
    """GET /api/v1/hits/?q=<query>&w=<weight>."""
    # (1) get query parameters
    query = request.args.get("q", "")
    weight_str = request.args.get("w", default="0.5")
    try:
        weight = float(weight_str)
    except ValueError:
        weight = 0.5

    # clamp weight to [0, 1] just to be safe
    if weight < 0.0:
        weight = 0.0
    elif weight > 1.0:
        weight = 1.0

    # (2) clean and tokenize query (same rules as pipeline)
    text = CLEAN_RE.sub("", query)  # remove punctuation etc.
    text = text.casefold()          # lowercase
    tokens = [t for t in text.split() if t and t not in STOPWORDS]

    # no terms left after cleaning/stopwords
    if not tokens:
        return jsonify({"hits": []})

    # (3) term frequency in query
    q_tf = Counter(tokens)

    # AND semantics: all terms must be present in this segment
    for term in q_tf:
        if term not in INVERTED_INDEX:
            return jsonify({"hits": []})

    # (4) build query vector weights: w_q_t = TF * IDF
    q_weights = {}
    for term, freq in q_tf.items():
        entry = INVERTED_INDEX[term]
        idf = entry["idf"]
        q_weights[term] = freq * idf  # float

    # query normalization
    q_norm_sq = sum(w * w for w in q_weights.values())
    if q_norm_sq == 0.0:
        return jsonify({"hits": []})
    q_norm = math.sqrt(q_norm_sq)

    # Pre-normalized query unit weights
    q_unit = {t: (w / q_norm) for t, w in q_weights.items()}

    # (5) find candidate docs: intersection of doc sets for all terms
    doc_sets = [
        set(INVERTED_INDEX[term]["docs"].keys())
        for term in q_tf
    ]
    candidates = set.intersection(*doc_sets) if doc_sets else set()
    if not candidates:
        return jsonify({"hits": []})

    results = []

    # (6) score each candidate document
    for docid in candidates:
        tfidf_sim = 0.0

        for term in q_tf:
            entry = INVERTED_INDEX[term]
            idf = entry["idf"]
            posting = entry["docs"][docid]
            tf = posting["tf"]
            doc_len = posting["doc_len"]

            if doc_len == 0.0:
                continue  # safety, shouldn't happen

            # normalized document weight
            w_d = (tf * idf) / doc_len
            # normalized query weight
            w_q = q_unit[term]

            tfidf_sim += w_d * w_q

        # (7) incorporate PageRank
        pr_score = PAGERANK.get(docid, 0.0)
        final_score = (1.0 - weight) * tfidf_sim + weight * pr_score

        results.append({
            "docid": int(docid),
            "score": final_score,
        })

    # (8) sort results by score descending
    # (tie-break on docid for determinism; not required but nice)
    results.sort(key=lambda x: (-x["score"], x["docid"]))

    return jsonify({"hits": results})
