from flask import request, jsonify, make_response

from app import app, db
from app.model import Book, Author


def initialize_database():
    db.drop_all()
    db.create_all()

    book1 = Book(title="Hobbit czyli Tam i z powrotem",
                 acquired=False,
                 published_year="2004")
    insert_record(book1)

    author1 = Author(name="J. R. R. Tolkien", book=book1)
    insert_record(author1)

    book2 = Book(title="A Middle English Reader",
                 acquired=False,
                 published_year="2005")
    insert_record(book2)

    author2 = Author(name="J. R. R. Tolkien", book=book2)
    insert_record(author2)

    author3 = Author(name="Kenneth Sisam", book=book2)
    insert_record(author3)


def insert_record(record):
    db.session.add(record)
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
