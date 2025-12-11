import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from models import Book
from schemas import BookCreate, BookResponse, BookUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)) -> Book:
    logger.info(f"Creating book: {book.title} by {book.author}")
    try:
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        logger.info(f"Book created with ID: {db_book.id}")
        return db_book
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating book: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create book")


@router.get("/books/", response_model=list[BookResponse])
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
) -> list[Book]:
    logger.info(f"Fetching books: skip={skip}, limit={limit}")
    books = db.query(Book).offset(skip).limit(limit).all()
    logger.info(f"Returned {len(books)} books")
    return books


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)) -> Book:
    logger.info(f"Updating book with ID: {book_id}")
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        logger.warning(f"Book with ID {book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")

    try:
        update_data = book_update.model_dump(exclude_unset=True)  # Only include fields that were explicitly provided
        logger.info(f"Updating fields: {list(update_data.keys())}")
        for field, value in update_data.items():
            setattr(db_book, field, value)

        db.commit()
        db.refresh(db_book)
        logger.info(f"Book {book_id} updated successfully")
        return db_book
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update book")


@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    logger.info(f"Deleting book with ID: {book_id}")
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        logger.warning(f"Book with ID {book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")

    try:
        db.delete(db_book)
        db.commit()
        logger.info(f"Book {book_id} deleted successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete book")


@router.get("/books/search/", response_model=list[BookResponse])
def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    year: Optional[int] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
) -> list[Book]:
    search_params = {k: v for k, v in {"title": title, "author": author, "year": year}.items() if v}
    logger.info(f"Searching books with params: {search_params}, skip={skip}, limit={limit}")

    query = db.query(Book)

    filters = []
    if title:
        filters.append(Book.title.ilike(f"%{title}%"))  # Case-insensitive partial match
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))  # Case-insensitive partial match
    if year:
        filters.append(Book.year == year)

    if filters:
        query = query.filter(or_(*filters))  # Combine multiple search conditions with OR logic

    books = query.offset(skip).limit(limit).all()
    logger.info(f"Search returned {len(books)} books")
    return books
