from fastapi import FastAPI
from . api.books_router import router as books_router

app = FastAPI(title="Books API (DDD)")

app.include_router(books_router)
