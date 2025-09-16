from pydantic import BaseModel

class UpdateBookDTO(BaseModel):
    nome: str | None = None
    autor: str | None = None
    ano: int | None = None
    editora: str | None = None
    isbn: str | None = None
