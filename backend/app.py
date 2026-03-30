from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load data
with open("../books.json") as f:
    books = json.load(f)


@app.route("/")
def home():
    return "📚 BookScope API Running"


@app.route("/books")
def get_books():
    return jsonify(books)


# 🔍 Filter by rating
@app.route("/books/filter")
def filter_books():
    rating = request.args.get("rating")
    category = request.args.get("category")

    filtered = books

    if rating:
        filtered = [b for b in filtered if b["rating"] == int(rating)]

    if category:
        filtered = [b for b in filtered if b["category"].lower() == category.lower()]

    return jsonify(filtered)


if __name__ == "__main__":
    app.run(debug=True)