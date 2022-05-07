from dataclasses import dataclass
from sqlalchemy import Column, Integer, String

from . import db


class Book(db.Model):
    id = Column("id", Integer, primary_key=True)
    title = Column(String(100), nullable=False)

    def __init__(self, title):
        self.title = title

    # def __str__(self):
    #     return f"Book({self.title})"
    #
    # def __eq__(self, other):
    #     if isinstance(self, other.__class__):
    #         return self.title == other.title
    #     else:
    #         return False

    def to_json(self):
        return {
            "title": self.title
        }
