from .. dtos.create_book_dto import CreateBookDTO
from .. dtos.read_book_dto import ReadBookDTO
from .. contracts.uow import UnitOfWork
from ... domain.entities.book import Book
from ... domain.value_objects.isbn import ISBN

def _to_read_dto(book: Book) -> ReadBookDTO:
    return ReadBookDTO(
        id=book.id, 
        nome=book.nome, 
        autor=book.autor, 
        ano=book.ano, 
        editora=book.editora, 
        isbn=book.isbn.text
    )

async def create_book(uow: UnitOfWork, payload: CreateBookDTO) -> ReadBookDTO:
    async with uow:
        isbn_vo = await create_valid_isbn(uow, payload)
        book = Book(
            id=None,
            nome=payload.nome,
            autor=payload.autor,
            ano=payload.ano,
            editora=payload.editora,
            isbn=isbn_vo
        )
        saved = await uow.books.add(book)
        await uow.commit()
        return _to_read_dto(saved)

async def create_valid_isbn(uow, payload):
    isbn_vo = ISBN(payload.isbn)
    exists = await uow.books.get_by_isbn(isbn_vo.normalized())
    if exists:
        raise ValueError("Já existe um livro com esse ISBN.")
    return isbn_vo
