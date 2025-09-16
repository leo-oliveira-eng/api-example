from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, UniqueConstraint

class Base(DeclarativeBase):
    pass

class BookORM(Base):
    __tablename__ = "books"
    __table_args__ = (UniqueConstraint("isbn_norm", name="uq_books_isbn_norm"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    autor: Mapped[str] = mapped_column(String(200), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    editora: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False)       # original
    isbn_norm: Mapped[str] = mapped_column(String(20), nullable=False)  # normalizado para índice único
