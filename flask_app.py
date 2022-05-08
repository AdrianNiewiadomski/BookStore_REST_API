from flask import request

from app import app
from app.controller import Controller
from app.orm import initialize_database


@app.route("/books", methods=["GET"])
def get_books():
    return Controller(request).get_books_response()


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id: int):
    return Controller.get_book_by_id_response(book_id)


@app.route("/books/<int:book_id>", methods=["PATCH"])
def update_book_by_id(book_id: int):
    return Controller(request).update_book_by_id(book_id)


initialize_database()

if __name__ == '__main__':
    app.run(debug=True)
