from flask import request, jsonify, make_response

from app import app, db
from app.model import Book


def initialize_database():
    db.drop_all()
    db.create_all()

    book = Book("Hobbit czyli Tam i z powrotem")
    insert_book(book)


def insert_book(book):
    db.session.add(book)
    db.session.commit()


@app.route("/books", methods=["GET"])
def get_books():
    if not request.args:
        books = get_all_books()
        response = make_response(jsonify([book.to_json() for book in books]))
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        return request.args


def get_all_books():
    return Book.query.all()


@app.route("/books/<int:book_id>", methods=["GET"])
def display_number(book_id: int):
    book = Book.query.filter_by(id=book_id).first()
    return book.to_json()


initialize_database()

if __name__ == '__main__':
    app.run(debug=True)
