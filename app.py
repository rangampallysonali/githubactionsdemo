from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client["library"]
books = db["books"]

@app.route("/")
def home():
    return "Book API is running"

@app.route("/books", methods=["GET"])
def get_books():
    all_books = []
    for book in books.find({}, {"_id": 0}):
        all_books.append(book)
    return jsonify(all_books)

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    book = {
        "id": data["id"],
        "title": data["title"],
        "author": data["author"]
    }

    result = books.insert_one(book)

    return jsonify({
        "message": "Book added",
        "book": {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"]
        },
        "mongo_id": str(result.inserted_id)
    }), 200

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    result = books.delete_one({"id": book_id})

    if result.deleted_count == 0:
        return jsonify({"message": "Book not found"}), 404

    return jsonify({"message": "Book deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)