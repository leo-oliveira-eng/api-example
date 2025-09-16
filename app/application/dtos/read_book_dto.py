from pydantic import BaseModel, ConfigDict

class ReadBookDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    autor: str
    ano: int
    editora: str
    isbn: str