from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from . import db


class Book(db.Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(String(12), nullable=False)
    title = Column(String(100), nullable=False)
    authors = db.relationship('Author', backref='book')
    published_year = Column(String(4), nullable=False)
    acquired = Column(Boolean, nullable=False)
    thumbnail = Column(String(100))

    def to_dict(self) -> dict:
        authors = [author.to_string() for author in self.authors]
        return {
            "id": self.id,
            "title": self.title,
            "authors": authors,
            "acquired": self.acquired,
            "published_year": self.published_year
        }

    def all_data_to_dict(self) -> dict:
        data = self.to_dict()
        data["external_id"] = self.external_id
        data["thumbnail"] = self.thumbnail
        return data


class Author(db.Model):
    author_id = Column("id", Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'))

    def to_string(self) -> Column:
        return self.name
