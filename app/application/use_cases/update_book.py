from .. dtos.update_book_dto import UpdateBookDTO
from .. dtos.read_book_dto import ReadBookDTO
from .. contracts.uow import UnitOfWork
from ... domain.value_objects.isbn import ISBN

async def update_book(uow: UnitOfWork, book_id: int, payload: UpdateBookDTO) -> ReadBookDTO | None:
    async with uow:
        book = await uow.books.get(book_id)
        if not book:
            return None

        data = payload.model_dump(exclude_unset=True)
        if "nome" in data: book.nome = data["nome"]
        if "autor" in data: book.autor = data["autor"]
        if "ano" in data: book.ano = data["ano"]
        if "editora" in data: book.editora = data["editora"]
        if "isbn" in data and data["isbn"]:            
            book.isbn = await _create_valid_isbn(uow, data["isbn"])

        updated = await uow.books.update(book)
        await uow.commit()
        return ReadBookDTO(id=updated.id, nome=updated.nome, autor=updated.autor, ano=updated.ano, editora=updated.editora, isbn=updated.isbn.text)

async def _create_valid_isbn(uow: UnitOfWork, isbn: str) -> ISBN:
    isbn_vo = ISBN(isbn)
    exists = await uow.books.get_by_isbn(isbn_vo.normalized())
    if exists and exists.isbn.normalized() != isbn_vo.normalized():
        raise ValueError("Já existe um livro com esse ISBN.")
    return isbn_vo