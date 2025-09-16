from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ... infrastructure.db.database import get_session, engine
from ... infrastructure.db.models import Base
from ... infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from ... application.dtos.create_book_dto import CreateBookDTO
from ... application.dtos.update_book_dto import UpdateBookDTO
from ... application.dtos.read_book_dto import ReadBookDTO
from ... application.use_cases.create_book import create_book
from ... application.use_cases.get_book import get_book
from ... application.use_cases.list_books import list_books
from ... application.use_cases.update_book import update_book
from ... application.use_cases.delete_book import delete_book

router = APIRouter(prefix="/books", tags=["Books"])

@router.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_uow(session: AsyncSession = Depends(get_session)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)

@router.post("", response_model=ReadBookDTO, status_code=status.HTTP_201_CREATED)
async def create(payload: CreateBookDTO, uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    try:
        return await create_book(uow, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[ReadBookDTO])
async def list_(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: Optional[str] = Query(None),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
):
    return await list_books(uow, skip, limit, q)

@router.get("/{book_id}", response_model=ReadBookDTO)
async def get_(book_id: int, uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    b = await get_book(uow, book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return b

@router.patch("/{book_id}", response_model=ReadBookDTO)
async def update_(book_id: int, payload: UpdateBookDTO, uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    try:
        b = await update_book(uow, book_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return b

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_(book_id: int, uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    ok = await delete_book(uow, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
