from sqlalchemy.ext.asyncio import AsyncSession
from ... application.contracts.uow import UnitOfWork
from ... domain.repositories.book_repository import BookRepository
from ... infrastructure.repositories.book_repository_impl import SqlAlchemyBookRepository

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.books: BookRepository = SqlAlchemyBookRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.rollback()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
