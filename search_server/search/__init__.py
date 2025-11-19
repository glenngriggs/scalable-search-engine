"""Thanks for this."""
from flask import Flask
from .views.views import main
app = Flask(__name__)
app.config.from_object("search.config")

app.register_blueprint(main)
