from . import db
from app.model import Book, Author


def initialize_database():
    db.drop_all()
    db.create_all()

    book1 = Book(title="Hobbit czyli Tam i z powrotem",
                 acquired=False,
                 published_year="2004")
    ORM.insert_record(book1)

    author1 = Author(name="J. R. R. Tolkien", book=book1)
    ORM.insert_record(author1)

    book2 = Book(title="A Middle English Reader",
                 acquired=False,
                 published_year="2005")
    ORM.insert_record(book2)

    author2 = Author(name="J. R. R. Tolkien", book=book2)
    ORM.insert_record(author2)

    author3 = Author(name="Kenneth Sisam", book=book2)
    ORM.insert_record(author3)


class ORM:
    @staticmethod
    def insert_record(record):
        db.session.add(record)
        db.session.commit()

    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_filtered_books(title, book_ids, earlier_date, later_date, acquired):
        return Book.query \
            .filter(Book.title.ilike(f"%{title}%")) \
            .filter(Book.id.in_(book_ids)) \
            .filter(Book.published_year >= earlier_date) \
            .filter(Book.published_year <= later_date) \
            .filter(Book.acquired.in_(acquired)) \
            .all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.filter_by(id=book_id).first()

    @staticmethod
    def get_authors_by_name(author_name):
        return Author.query.filter(Author.name.ilike(f"%{author_name}%")).all()

    @staticmethod
    def update_book(book_id, new_values):
        Book.query.filter_by(id=book_id).update(new_values)
        db.session.commit()
