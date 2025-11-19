# Distributed Search Engine (MapReduce + TF-IDF + PageRank)

A fully functional distributed search engine that processes a multi-thousand–document web crawl using a MapReduce pipeline, builds a segmented inverted index, exposes a REST API for scoring and retrieval, and serves a dynamic HTML search interface similar to Google/Bing.

Demonstrates information retrieval (IR), large-scale data processing, concurrency, and service-oriented architecture concepts.

---

## Overview

This project implements a complete search engine stack consisting of:

1. **Inverted Index Pipeline (MapReduce):**  
   A sequence of Python MapReduce jobs run using Michigan Hadoop (Madoop) to compute:  
   - tokenization + normalization  
   - term frequency (TF)  
   - inverse document frequency (IDF)  
   - document vector norms  
   - segmented posting lists  
   - final TF-IDF weights  
   - custom partitioning into 3 index files  
   These outputs match the instructor specification for format and segment generation.

2. **Index Server (REST API):**  
   A Flask service that loads one index segment into memory and returns ranked search results as JSON.  
   - `/api/v1/` – service descriptor  
   - `/api/v1/hits/?q=query&w=weight` – tf-idf + PageRank scoring  
   - Loads inverted index, PageRank, and stopwords once at startup for efficiency.

3. **Search Server (Dynamic UI):**  
   A server-side rendered search UI using Flask templates.  
   - Query input  
   - PageRank weight slider  
   - Top-10 result display  
   - Parallel fetches to all index segments using threads  
   - Combines and re-ranks results from all segments.

Together, these components form a production-style distributed search pipeline with a clean modular design.

---

## System Architecture

### High-Level Flow
```
                ┌────────────────────┐
                │ Web Crawl (HTML)   │
                └─────────┬──────────┘
                          │
                [MapReduce Pipeline]
                          │
         ┌────────────────▼────────────────┐
         │ Segmented Inverted Index (3x)   │
         └────────────────┬────────────────┘
                          │
         [Index Servers: 9000 / 9001 / 9002]
                          │
                [Search Server UI]
                          │
            Renders Top-10 HTML Results
```

---

## Inverted Index Pipeline (MapReduce)

The inverted index is generated through a multi-job MapReduce pipeline using Madoop.  
Jobs include:

### **Job 0: Document Counting**  
Counts total documents in the crawl directory based on `<!DOCTYPE html>` occurrences.  
Output: `total_document_count.txt`

### **Job 1: HTML Parsing & Token Extraction**  
Uses BeautifulSoup to extract:
- `docid`
- page text content (cleaned, lower-cased, stopwords removed)  
This normalizes HTML documents into clean token streams.

### **Job 2–N: TF, IDF, Norms, and Posting List Construction**  
Each job transforms intermediate representations:
- term frequencies per doc  
- inverse document frequencies (log base 10)  
- normalization factors (vector magnitudes)  
- grouped postings per term  
- custom partitioning by `doc_id % 3` using partition logic.

Final output of the pipeline:
```
inverted_index_0.txt
inverted_index_1.txt
inverted_index_2.txt
```
Each file contains:
```
term idf docid tf norm [docid tf norm]...
```

This segmented design enables horizontal scaling of the Index server.

---

## Index Server (REST API)

Each Index server instance loads **one** of the 3 index segments.  
Key functionality:

### **Endpoints**
- `GET /api/v1/`  
  Returns available API routes.

- `GET /api/v1/hits/?q=...&w=...`  
  Returns ranked documents with:
  - Cosine similarity (TF-IDF)  
  - PageRank integration  
  - Combined weighted score  
  - Sorted descending relevance  

Queries with multiple terms behave as **AND queries** (non-phrase).

### **Scoring Formula**
```
Score(q, d, w) = w * PageRank(d) + (1 - w) * cosSim(q, d)
```
where:
- `w` ∈ [0,1] is PageRank weight  
- `cosSim(q, d)` uses normalized tf-idf vectors  

---

## Search Server (UI)

The search server renders an interactive page:

### **Features**
- Clean HTML search bar  
- Slider for PageRank weight  
- Dynamic GET-based query  
- Parallel querying of all Index servers  
- Aggregation + re-ranking of results  
- Top-10 display with:
  - document title  
  - summary  
  - clickable URL  
  - fallback “No summary available” text  

---

## Directory Structure (Simplified)

```
.
├── inverted_index/
│   ├── map*.py
│   ├── reduce*.py
│   ├── pipeline.sh
│   ├── stopwords.txt
│   ├── crawl/
│   └── output/
│
├── index_server/
│   ├── index/
│   │   ├── api/
│   │   ├── inverted_index/
│   │   ├── pagerank.out
│   │   └── stopwords.txt
│   └── pyproject.toml
│
├── search_server/
│   ├── search/
│   │   ├── templates/
│   │   ├── static/
│   │   ├── config.py
│   │   ├── model.py
│   │   └── views/
│   └── pyproject.toml
│
├── bin/
│   ├── index
│   ├── search
│   └── searchdb
```

---

## Testing

The project includes a comprehensive public test suite covering:

- MapReduce pipeline correctness  
- Segment generation  
- Index server API correctness  
- PageRank/TF-IDF scoring  
- Search UI rendering  
- SQLite population via `searchdb`  

All Python modules conform to:
- Pylint  
- Pydocstyle  
- Pycodestyle  

---

## Installation

```bash
./bin/install
```

---

## Running

### Create SQLite searchDB

```bash
./bin/searchdb
```

### Start Index Servers (all 3 segments)
```bash
./bin/index start
```

### Start Search Server
```bash
./bin/search start
```

Go to:
```
http://localhost:8000/
```

---
