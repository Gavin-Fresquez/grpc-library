from dataclasses import dataclass

@dataclass
class Book:
    id: str
    title: str
    author: str
    description: str
    isbn_number: int
    checked_out: bool

    def get_tuple(self) -> tuple[str, str, str, str, int, bool]:
        return self.id, self.title, self.author, self.description, self.isbn_number, self.checked_out

    def get_tuple_id_last(self) -> tuple[str, str, str, int, bool, str]:
        return self.title, self.author, self.description, self.isbn_number, self.checked_out, self.id

