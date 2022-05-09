import json
from datetime import date
from typing import List
from typing import Union

import requests
from flask import make_response, jsonify, Response

from .decorator import loop_through_authors
from .model import Book
from .orm import ORM


class Controller:
    def __init__(self, request):
        self.args = request.args
        self.body = json.loads(
            request.data.decode('utf8')) if request.data else None

    def get_books_response(self) -> Response:
        if not self.args:
            books = ORM.get_all_books()
        else:
            books = self._get_filtered_books()

        return Controller._get_response([book.to_dict() for book in books],
                                        200)

    def _get_filtered_books(self) -> List[Book]:
        title, book_ids, earlier_date, later_date, acquired \
            = self._extract_arguments()
        return ORM.get_filtered_books(title, book_ids, earlier_date,
                                      later_date, acquired)

    def _extract_arguments(self) -> tuple:
        title = self.args.get("title", "").replace("\"", "")
        book_ids = self._get_book_ids_by_author_name()
        earlier_date = self.args.get("from", "0000")
        later_date = self.args.get("to", str(date.today().year))
        acquired = self._get_acquired_state()

        return title, book_ids, earlier_date, later_date, acquired

    def _get_book_ids_by_author_name(self) -> List[int]:
        author_name = self.args.get("author", "").replace("\"", "")
        authors = ORM.get_authors_by_name(author_name)
        return [author.book_id for author in authors]

    def _get_acquired_state(self) -> tuple:
        if self.args.get("acquired"):
            return (json.loads(self.args.get("acquired")),)
        else:
            return True, False

    @staticmethod
    def _get_response(response_data: Union[dict, list], status_code: int) -> \
            Response:
        response = make_response(jsonify(response_data), status_code)
        response.headers["Content-Type"] = "application/json"
        return response

    @staticmethod
    def get_book_by_id_response(book_id: int) -> Union[dict, Response]:
        book = ORM.get_book_by_id(book_id)
        if book:
            return book.all_data_to_dict()

        return Controller._get_response(
            {"error_description":
             "The requested resource could not be found."},
            404)

    def update_book_by_id(self, book_id: int) -> Union[dict, Response]:
        ORM.update_book_by_id(book_id, self.body)
        return self.get_book_by_id_response(book_id)

    @staticmethod
    def delete_book_by_id(book_id: int) -> Response:
        ORM.delete_book_by_id(book_id)
        return Controller._get_response({}, 204)

    def import_books_by_author_name(self) -> Union[dict, Response]:
        author = self.body["author"]
        result = requests.get(
            "https://www.googleapis.com/books/v1/volumes?q=inauthor:'{}'"
            .format(author)
        )

        if result.ok:
            imported_books = result.json()["items"]

            number_of_imported_books = 0
            try:
                for imported_book in imported_books:
                    number_of_imported_books = Controller \
                        ._process_imported_book(imported_book,
                                                number_of_imported_books)
                return {"imported": number_of_imported_books}
            except KeyError:
                return Controller._get_response(
                    {"error_description":
                     "The response does not have the required fields."},
                    404)
        else:
            return Controller._get_response(
                {"error_description":
                 "The required resource cannot be found."},
                404)

    @staticmethod
    def _process_imported_book(imported_book: dict,
                               number_of_imported_books: int) -> int:
        imported_values = Controller._get_book_details(imported_book)

        old_book = ORM.get_filtered_books_by_external_id(
            imported_values["external_id"])
        if old_book:
            Controller._update_imported_book(old_book, imported_values,
                                             imported_book)
        else:
            Controller._insert_imported_book(imported_book, imported_values)

        number_of_imported_books += 1
        return number_of_imported_books

    @staticmethod
    def _get_book_details(imported_book: dict) -> dict:
        title = imported_book["volumeInfo"]["title"]
        published_date = imported_book["volumeInfo"]["publishedDate"]
        if "-" in published_date:
            published_year = published_date[:published_date.find("-")]
        else:
            published_year = published_date
        external_id = imported_book["id"]
        thumbnail = imported_book["accessInfo"]["webReaderLink"]
        return {"title": title, "published_year": published_year,
                "external_id": external_id, "thumbnail": thumbnail}

    @staticmethod
    def _update_imported_book(old_book: Book, imported_values: dict,
                              imported_book: dict) -> None:
        ORM.update_book_by_id(old_book.id, imported_values)
        old_authors = ORM.get_authors_by_book_id(old_book.id)
        new_authors = imported_book["volumeInfo"]["authors"]

        authors_to_be_updated = list(zip(old_authors, new_authors))
        for old, new in authors_to_be_updated:
            ORM.update_author(old, {"name": new})

        @loop_through_authors
        def delete_authors(args):
            ORM.delete_author_by_id(args[0].author_id)

        @loop_through_authors
        def insert_authors(args):
            ORM.create_author(args[0], args[1])

        delete_authors(authors_to_be_updated, old_authors)
        insert_authors(authors_to_be_updated, new_authors, old_book)

    @staticmethod
    def _insert_imported_book(imported_book: dict,
                              imported_values: dict) -> None:
        book = ORM.create_book(**imported_values, acquired=False)
        authors = imported_book["volumeInfo"]["authors"]

        for author_name in authors:
            ORM.create_author(author_name, book)
