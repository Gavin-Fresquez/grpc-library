from abc import ABC, abstractmethod

from models import Book


INSERT_QUERY = 'insert into books (id,title,author,description,isbn_number,checked_out) values (%s,%s,%s,%s,%s,%s)'
UPDATE_QUERY = 'update books set title=%s,author=%s,description=%s,isbn_number=%s,checked_out=%s where id=%s'
GET_QUERY = 'select id,title,author,description,isbn_number,checked_out from books where id=%s'
DELETE_QUERY = 'delete from books where id=%s'

class IBookRepository(ABC):
    """Book repository interface"""

    @abstractmethod
    def create_book(self, book: Book) -> str:
        pass

    @abstractmethod
    def update_book(self, book: Book) -> str:
        pass

    @abstractmethod
    def get_book_by_id(self, id: str) -> Book:
        pass

    @abstractmethod
    def get_book_by_isbn(self, isbn: int) -> Book:
        pass

    @abstractmethod
    def delete_book_by_id(self, id: str) -> bool:
        pass

    @abstractmethod
    def delete_book_by_isbn(self, isbn: int) -> bool:
        pass


class BookRepository(IBookRepository):
    """Concrete implementation of IBookRepository"""

    def __init__(self, db):
        self._db = db

    def create_book(self, book: Book) -> str:
        cursor = self._db.cursor()
        cursor.execute(INSERT_QUERY, book.get_tuple())
        self._db.commit()
        return book.id

    def update_book(self, book: Book) -> str:
        cursor = self._db.cursor()
        cursor.execute(UPDATE_QUERY, book.get_tuple_id_last()) # id needs to come last, see models/book.py for method docs
        self._db.commit()
        return book.id

    def get_book_by_id(self, id: str) -> Book:
        cursor = self._db.cursor()
        cursor.execute(GET_QUERY, (id,))
        row = cursor.fetchone()
        return Book(*row)

    def get_book_by_isbn(self, isbn: int) -> Book:
        cursor = self._db.cursor()
        cursor.execute(GET_QUERY, (isbn,))
        row = cursor.fetchone()
        return Book(*row)

    def delete_book_by_id(self, id: str) -> bool:
        cursor = self._db.cursor()
        cursor.execute(DELETE_QUERY, (id,))
        self._db.commit()
        return True

    def delete_book_by_isbn(self, isbn: int) -> bool:
        cursor = self._db.cursor()
        cursor.execute(DELETE_QUERY, (isbn,))
        self._db.commit()
        return True

