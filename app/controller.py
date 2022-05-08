import json
from datetime import date
from flask import make_response, jsonify

from .orm import ORM


class Controller:
    def __init__(self, request):
        self.args = request.args
        self.body = json.loads(request.data.decode('utf8')) if request.data else None

    def get_books_response(self):
        if not self.args:
            books = ORM.get_all_books()
        else:
            books = self._get_filtered_books()

        response = make_response(jsonify([book.to_dict() for book in books]))
        response.headers["Content-Type"] = "application/json"
        return response

    def _get_filtered_books(self):
        title, book_ids, earlier_date, later_date, acquired = self._extract_arguments()
        return ORM.get_filtered_books(title, book_ids, earlier_date, later_date, acquired)

    def _extract_arguments(self):
        title = self.args.get("title", "").replace("\"", "")
        book_ids = self._get_book_ids_by_author_name()
        earlier_date = self.args.get("from", "0000")
        later_date = self.args.get("to", str(date.today().year))
        acquired = self._get_acquired_state()

        return title, book_ids, earlier_date, later_date, acquired

    def _get_book_ids_by_author_name(self):
        author_name = self.args.get("author", "").replace("\"", "")
        authors = ORM.get_authors_by_name(author_name)
        return [author.book_id for author in authors]

    def _get_acquired_state(self):
        if self.args.get("acquired"):
            return (json.loads(self.args.get("acquired")),)
        else:
            return True, False

    @staticmethod
    def get_book_by_id_response(book_id):
        book = ORM.get_book_by_id(book_id)
        return book.to_dict()

    def update_book_by_id(self, book_id):
        ORM.update_book_by_id(book_id, self.body)
        return self.get_book_by_id_response(book_id)

    @staticmethod
    def delete_book_by_id(book_id):
        ORM.delete_book_by_id(book_id)
        return '', 204
