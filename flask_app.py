import json

from flask import request, jsonify, make_response

from app import app, db
from app.model import Book, Author
from datetime import date

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
    else:
        title = request.args.get("title", "").replace("\"", "")

        author_name = request.args.get("author", "").replace("\"", "")
        print("author_name: ", author_name)
        authors = Author.query.filter(Author.name.ilike(f"%{author_name}%")).all()
        book_ids = [author.book_id for author in authors]

        earlier_date = request.args.get("from", "0000")
        later_date = request.args.get("to", str(date.today().year))

        if request.args.get("acquired"):
            acquired = (json.loads(request.args.get("acquired")), )
        else:
            acquired = (True, False)

        books = Book.query \
            .filter(Book.title.ilike(f"%{title}%")) \
            .filter(Book.book_id.in_(book_ids)) \
            .filter(Book.published_year >= earlier_date) \
            .filter(Book.published_year <= later_date) \
            .filter(Book.acquired.in_(acquired)) \
            .all()

    response = make_response(jsonify([book.to_json() for book in books]))
    response.headers["Content-Type"] = "application/json"
    return response


def get_all_books():
    return Book.query.all()


@app.route("/books/<int:book_id>", methods=["GET"])
def display_number(book_id: int):
    book = Book.query.filter_by(book_id=book_id).first()
    return book.to_json()


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
