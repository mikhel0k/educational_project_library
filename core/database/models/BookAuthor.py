from sqlalchemy import Table, Column, Integer, ForeignKey
from .Base import BaseModel


book_author = Table(
    'book_author',
    BaseModel.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True),
)
