#!/usr/bin/env python3
"""Search server views: main search page and integration with Index servers."""

from flask import Blueprint, request, render_template, current_app
import urllib.parse
import sqlite3
import concurrent.futures
import requests
import search.config as config

# Blueprint for all search routes
main = Blueprint("main", __name__)


def fetch_hits(url, query, weight):
    """Fetch is for you deorio thanks."""
    params = {"q": query, "w": weight}
    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        payload = resp.json()
        return payload.get("hits", [])
    except requests.RequestException:
        return []


def get_all_hits(query, weight):
    """
    Query all index segments in parallel and collect their hits.

    Reads SEARCH_INDEX_SEGMENT_API_URLS from the Flask app config first,
    falling back to search.config.SEARCH_INDEX_SEGMENT_API_URLS.

    Args:
        query: Raw query string.
        weight: PageRank weight.

    Returns:
        A single flat list of hit dicts from all segments.
    """
    # Prefer live config from the app (tests may override this),
    # fall back to the module-level default in search.config.
    urls = current_app.config.get(
        "SEARCH_INDEX_SEGMENT_API_URLS",
        getattr(config, "SEARCH_INDEX_SEGMENT_API_URLS", []),
    )

    if not urls:
        return []

    hits = []
    # One worker per URL so all segments can be queried concurrently
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(urls)
    ) as executor:
        futures = [
            executor.submit(fetch_hits, url, query, weight) for url in urls
        ]
        for fut in concurrent.futures.as_completed(futures):
            segment_hits = fut.result()
            if segment_hits:
                hits.extend(segment_hits)

    return hits


def fetch_doc_info(docid):
    """Look up document metadata (title, summary, url) for a given docid."""
    db_path = current_app.config.get("SEARCH_DB_PATH", "var/search.sqlite3")

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT title, summary, url FROM documents WHERE docid = ?",
            (docid,),
        )
        row = cur.fetchone()

    if row:
        title, summary, url = row
        title = title or ""
        summary = summary or ""
        url = url or ""
        return {
            "docid": docid,
            "title": title,
            "summary": summary,
            "url": url,
            # Decoded URL text for display in <a class="doc_url">...</a>
            "url_display": urllib.parse.unquote(url),
        }

    # If document metadata is missing, return blanks
    return {
        "docid": docid,
        "title": "",
        "summary": "",
        "url": "",
        "url_display": "",
    }


@main.route("/", methods=["GET"])
def index():
    """Route search page (GET /)."""
    query = request.args.get("q", "")
    weight = request.args.get("w", "0.5")

    results = []

    # Only perform a search if there is a non-empty query string.
    if (query or "").strip():
        all_hits = get_all_hits(query, weight)

        all_hits.sort(
            key=lambda h: (
                -float(h.get("score", 0.0)),
                int(h.get("docid", 0)),
            )
        )

        top_hits = all_hits[:10]

        # Fetch metadata for each top docid
        results = [fetch_doc_info(hit["docid"]) for hit in top_hits]

    # Render GUI template
    return render_template(
        "index.html", results=results, query=query, weight=weight
    )
