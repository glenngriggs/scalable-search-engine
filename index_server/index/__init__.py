"""Flask API endpoints for the inverted index search."""
from pathlib import Path  # noqa: E402 pylint: disable=wrong-import-position
import os  # noqa: E402 pylint: disable=wrong-import-position
# import index.api

from flask import Flask

app = Flask(__name__)

# configure which inverted index
INDEX_DIR = Path(__file__).parent/"inverted_index"
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH",  # Environment variable name
    INDEX_DIR/"inverted_index_1.txt"  # Default value
)

# Import API AFTER app is created?
import index.api  # noqa: E402 pylint: disable=wrong-import-position

# Load index/pagerank/stopwords into memory
index.api.register_blueprints(app)
index.api.load_index()
