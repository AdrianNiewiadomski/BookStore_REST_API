from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from . import db


class Book(db.Model):
    id = Column(Integer, primary_key=True)

    title = Column(String(100), nullable=False)
    acquired = Column(Boolean, nullable=False)
    published_year = Column(String(4), nullable=False)

    authors = db.relationship('Author', backref='book')

    def to_dict(self) -> dict:
        authors = [author.to_string() for author in self.authors]
        return {
            "id": self.id,
            "title": self.title,
            "authors": authors,
            "acquired": self.acquired,
            "published_year": self.published_year
        }


class Author(db.Model):
    author_id = Column("id", Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'))

    def to_string(self):
        return self.name
