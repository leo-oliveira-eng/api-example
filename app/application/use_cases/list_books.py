from typing import List
from .. dtos.read_book_dto import ReadBookDTO
from .. contracts.uow import UnitOfWork

async def list_books(uow: UnitOfWork, skip: int, limit: int, q: str | None) -> List[ReadBookDTO]:
    async with uow:
        books = await uow.books.list(skip=skip, limit=limit, q=q)
        return [ReadBookDTO(id=book.id, nome=book.nome, autor=book.autor, ano=book.ano, editora=book.editora, isbn=book.isbn.text) for book in books]