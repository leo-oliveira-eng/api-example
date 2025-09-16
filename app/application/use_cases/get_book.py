from .. dtos.read_book_dto import ReadBookDTO
from .. contracts.uow import UnitOfWork

async def get_book(uow: UnitOfWork, book_id: int) -> ReadBookDTO | None:
    async with uow:
        book = await uow.books.get(book_id)
        if not book:
            return None
        return ReadBookDTO(id=book.id, nome=book.nome, autor=book.autor, ano=book.ano, editora=book.editora, isbn=book.isbn.text)
