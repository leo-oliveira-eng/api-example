from .. contracts.uow import UnitOfWork

async def delete_book(uow: UnitOfWork, book_id: int) -> bool:
    async with uow:
        b = await uow.books.get(book_id)
        if not b:
            return False
        await uow.books.delete(book_id)
        await uow.commit()
        return True
