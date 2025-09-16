from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from ... domain.entities.book import Book
from ... domain.repositories.book_repository import BookRepository
from ... domain.value_objects.isbn import ISBN
from ... infrastructure.db.models import BookORM

def _to_domain(row: BookORM) -> Book:
    return Book(
        id=row.id,
        nome=row.nome,
        autor=row.autor,
        ano=row.ano,
        editora=row.editora,
        isbn=ISBN(row.isbn),
    )

def _to_orm(book: Book) -> BookORM:
    return BookORM(
        id=book.id, nome=book.nome, autor=book.autor, ano=book.ano, editora=book.editora,
        isbn=book.isbn.text, isbn_norm=book.isbn.normalized()
    )

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, book: Book) -> Book:
        obj = _to_orm(book)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return _to_domain(obj)

    async def get(self, id_: int) -> Book | None:
        obj = await self.session.get(BookORM, id_)
        return _to_domain(obj) if obj else None

    async def get_by_isbn(self, isbn_norm: str) -> Book | None:
        stmt = select(BookORM).where(BookORM.isbn_norm == isbn_norm)
        obj = (await self.session.execute(stmt)).scalar_one_or_none()
        return _to_domain(obj) if obj else None

    async def list(self, skip: int, limit: int, q: str | None) -> Sequence[Book]:
        stmt = select(BookORM).order_by(BookORM.id.desc()).offset(skip).limit(limit)
        if q:
            stmt = select(BookORM).where(BookORM.nome.ilike(f"%{q}%")).order_by(BookORM.id.desc()).offset(skip).limit(limit)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [ _to_domain(row) for row in rows ]

    async def update(self, book: Book) -> Book:
        stmt = (
            update(BookORM)
            .where(BookORM.id == book.id)
            .values(
                nome=book.nome,
                autor=book.autor,
                ano=book.ano,
                editora=book.editora,
                isbn=book.isbn.text,
                isbn_norm=book.isbn.normalized(),
            )
            .returning(BookORM)
        )
        obj = (await self.session.execute(stmt)).scalar_one()
        return _to_domain(obj)

    async def delete(self, id_: int) -> None:
        await self.session.execute(delete(BookORM).where(BookORM.id == id_))
