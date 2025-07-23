from abc import ABC, abstractmethod
from types import MethodType

from models import Book, IDType
from repository import BookRepository


class ILibrary(ABC):
    """Library application interface"""

    @abstractmethod
    def add_book(self, book: Book) -> str:
        pass

    @abstractmethod
    def get_book(self, id: str | int, id_type: IDType = IDType.UUID) -> Book | None:
        pass

    @abstractmethod
    def list_books(self, limit: int) -> list[Book]:
        pass

    @abstractmethod
    def checkout_book(self, id: str | int, id_type: IDType = IDType.UUID) -> str:
        pass

    @abstractmethod
    def return_book(self, id: str | int, id_type: IDType = IDType.UUID) -> str:
        pass

    @abstractmethod
    def update_book(self, book: Book) -> str:
        pass

    @abstractmethod
    def delete_book(self, id: str | int, id_type: IDType = IDType.UUID) -> bool:
        pass


class Library(ILibrary):
    """Library application implementation"""

    def __init__(self, book_repository: BookRepository):
        self._book_repository = book_repository

    def add_book(self, book: Book) -> str:
        return self._book_repository.create_book(book)

    def get_book(self, id: str | int, id_type: IDType = IDType.UUID) -> Book | None:
        get_func = self._resolve_repository_get_method(id_type)
        if get_func:
            return get_func(id)
        return None

    def list_books(self, limit: int) -> list[Book]:
        return super().list_books(limit)

    def checkout_book(self, id: str | int, id_type: IDType = IDType.UUID) -> str:
        get_func = self._resolve_repository_get_method(id_type)
        if get_func:
            book = get_func(id)
            book.checked_out = True
            return self.update_book(book)
        return ''

    def return_book(self, id: str | int, id_type: IDType = IDType.UUID) -> str:
        get_func = self._resolve_repository_get_method(id_type)
        if get_func:
            book = get_func(id)
            book.checked_out = False
            return self.update_book(book)
        return ''

    def update_book(self, book: Book) -> str:
        return self._book_repository.update_book(book)

    def delete_book(self, id: str | int, id_type: IDType = IDType.UUID) -> bool:
        delete_func = self._resolve_repository_delete_method(id_type)
        if delete_func:
            return delete_func(id)
        return False

    def _resolve_repository_get_method(self, id_type: IDType) -> MethodType | None:
        match id_type:
            case IDType.UUID:
                return self._book_repository.get_book_by_id
            case IDType.ISBN:
                return self._book_repository.get_book_by_isbn

    def _resolve_repository_delete_method(self, id_type: IDType) -> MethodType | None:
        match id_type:
            case IDType.UUID:
                return self._book_repository.delete_book_by_id
            case IDType.ISBN:
                return self._book_repository.delete_book_by_isbn

