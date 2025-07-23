from models import Book as mBook
from protogen import Book as pBook

def bookProtoToModel(book: pBook) -> mBook:
    return mBook(
        book.uuid,
        book.title,
        book.author,
        book.description,
        book.isbn_number,
        book.checked_out
    )


def bookModelToProto(book: mBook) -> pBook:
    return pBook(*book.get_tuple())

