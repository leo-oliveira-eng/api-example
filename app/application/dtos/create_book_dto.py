from pydantic import BaseModel

class CreateBookDTO(BaseModel):
    nome: str
    autor: str
    ano: int
    editora: str
    isbn: str