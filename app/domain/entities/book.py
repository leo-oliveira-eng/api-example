from dataclasses import dataclass
from . .value_objects.isbn import ISBN

@dataclass
class Book:
    id: int | None
    nome: str
    autor: str
    ano: int
    editora: str
    isbn: ISBN