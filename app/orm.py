from typing import Union, List, Tuple

from app.model import Book, Author
from . import db


def initialize_database() -> None:
    db.drop_all()
    db.create_all()

    book1 = ORM.create_book("Hobbit czyli Tam i z powrotem", "2004",
                            "LLSpngEACAAJ")
    ORM.create_author(name="Tolkien", book=book1)
    ORM.create_author(name="Kenneth Sisam", book=book1)
    ORM.create_author(name="Niewiadomski", book=book1)

    book2 = ORM.create_book("A Middle English Reader", "2005", "X78hLLg6__8C")
    ORM.create_author(name="J. R. R. Tolkien", book=book2)


class ORM:
    @staticmethod
    def create_book(title: str, published_year: str, external_id: str,
                    acquired: bool = False, thumbnail: str = "") -> Book:
        book = Book(external_id=external_id, title=title,
                    published_year=published_year, acquired=acquired,
                    thumbnail=thumbnail)
        ORM.insert_record(book)
        return book

    @staticmethod
    def insert_record(record: Union[Book, Author]) -> None:
        db.session.add(record)
        db.session.commit()

    @staticmethod
    def create_author(name: str, book: Book) -> None:
        author = Author(name=name, book=book)
        ORM.insert_record(author)

    @staticmethod
    def get_all_books() -> List[Book]:
        return Book.query.all()

    @staticmethod
    def get_filtered_books(title: str, book_ids: List[int], earlier_date: str,
                           later_date: str, acquired: Tuple[bool]) \
            -> List[Book]:
        return Book.query \
            .filter(Book.title.ilike(f"%{title}%")) \
            .filter(Book.id.in_(book_ids)) \
            .filter(Book.published_year >= earlier_date) \
            .filter(Book.published_year <= later_date) \
            .filter(Book.acquired.in_(acquired)) \
            .all()

    @staticmethod
    def get_book_by_id(book_id: int) -> Union[None, Book]:
        return Book.query.filter_by(id=book_id).first()

    @staticmethod
    def get_filtered_books_by_external_id(external_id: str) \
            -> Union[None, Book]:
        return Book.query.filter_by(external_id=external_id).first()

    @staticmethod
    def get_authors_by_name(author_name: str) -> List[Author]:
        return Author.query.filter(Author.name.ilike(f"%{author_name}%")).all()

    @staticmethod
    def get_authors_by_book_id(book_id: int) -> List[Author]:
        return Author.query.filter(Author.book_id == book_id).all()

    @staticmethod
    def update_book_by_id(book_id: int, new_values: dict) -> None:
        Book.query.filter_by(id=book_id).update(new_values)
        db.session.commit()

    @staticmethod
    def update_author(old_author: Author, new_values: dict) -> None:
        Author.query.filter(Author.author_id == old_author.author_id)\
            .update(new_values)
        db.session.commit()

    @staticmethod
    def delete_book_by_id(book_id: int) -> None:
        Book.query.filter_by(id=book_id).delete()
        db.session.commit()

    @staticmethod
    def delete_author_by_id(author_id: Author) -> None:
        Author.query.filter_by(author_id=author_id).delete()
        db.session.commit()
