#routers/books.py — APIRouter (like Views + URLs combined)

from app import database
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List


'''
#from fastapi import APIRouter,Depends,HTTPException,status
------------APIRouter

Used to create a group of routes.

Think of it's like DRF:

    urlpatterns = [...]

    or:

    router = DefaultRouter()
    router.register(...)

------------Depends

FastAPI's Dependency Injection system.

You'll use it here:

    db: Session = Depends(get_db)

Meaning:

FastAPI, please give this endpoint a database session.


---------HTTPException

Used when you want to return an error.

For example:

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

DRF equivalent:

    raise NotFound("Book not found")

'''

'''
from sqlalchemy.orm import Session
Session represents your database session.

Think roughly:

Django ORM
    ↓
database connection/query handling

SQLAlchemy
    ↓
Session
'''

import models 
import schemas 
from database import get_db 

'''
This creates a router for books.

Because:

    prefix="/books"

when you write:

    @router.get("/")

the actual URL becomes:

    /books/

And:

    @router.get("/{book_id}")

becomes:

    /books/{book_id}

tags=["Books"] is mainly for Swagger documentation.
'''
router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


'''
@router.post("/",response_model=schemas.BookResponse,status_code=status.HTTP_201_CREATED)
HTTP method = POST
URL = /books/
response = BookResponse
success status = 201

DRF Analogy: 
class BookCreateView(APIView):
    def post(...):
'''
@router.post("/",response_model=schemas.BookResponse,status_code=status.HTTP_201_CREATED)
def create_book(book:schemas.BookCreate,db:Session=Depends(get_db)):
  '''
    book: schemas.BookCreate

    Means:

    Request body must follow BookCreate if schemas.py

    If client sends:

        {
            "title": "Python",
            "author": "Tasin",
            "price": 20
        }

    FastAPI validates it automatically.

    You don't need like DRF:

        serializer.is_valid()

    Pydantic does it.
  '''


  '''

    db: Session = Depends(get_db)

    Means:

    Get a database session using get_db().

    So FastAPI essentially does:

        Request
        ↓
        get_db()
        ↓
        db
        ↓
        create_book(book, db)
  '''
  db_book=models.Book(**book.model_dump())
  '''
    book.model_dump()

    produces:

        {
            "title": "Python",
            "author": "Tasin",
            "price": 20,
            "in_stock": True
        }

    Then:

        **book.model_dump()

    unpacks it:

        models.Book(
            title="Python",
            author="Tasin",
            price=20,
            in_stock=True
        )

    So:

    Pydantic object
        ↓
    model_dump()
        ↓
    dictionary
        ↓
    SQLAlchemy object
  '''
  db.add(db_book)
  '''
    db.add(db_book)

    Means:

    Add this object to the database session.

    Similar conceptually to:

    serializer.save()
  '''
  db.commit()
  db.refresh(db_book)
  '''
    db.refresh(db_book)
    This reloads the object from the database.

    Why?

    Because after inserting:

        db_book

    didn't necessarily have the database-generated ID before commit.

    After refresh:

        db_book.id

    will contain something like:

    1
  '''
  return db_book#You're returning the SQLAlchemy object.

'''


'''



@router.get("/",response_model=List[schemas.BookResponse])
def get_books(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books 


@router.get("/{book_id}",response_model=schemas.BookResponse)
def get_books(book_id:int,db:Session=Depends(get_db)):
    book=db.query(models.Book).filter(models.Book.id==book_id).first()
    if book is None:
        raise HTTPException(status_code=404,detail="Book not found")
    return book 


@router.put("/{book_id}",response_model=schemas.BookResponse)
def update_book(book_id:int, book:schemas.BookCreate,db:Session=Depends(get_db)):
    db_book=db.query(models.Book).filter(models.Book.id=book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404,detail="Book not found")
    for key,value in book.model_dumpt().items():
        setattr(db_book,key,value)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.patch("/{book_id}",response_model=schemas.BookResponse)
def partial_update_book(book_id:int,book:schemas.BookUpdate,db:Session=Depends(get_db)):
    db_book=db.query(models.Book).filter(models.Book.id==book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404,detail="book not found")
    update_data = book.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(db_book,key,value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id:int,db:Session=Depends(get_db)):
    db_book=db.query(models.Book).filter(models.Book.id==book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404,detail="Book not found")
    db.delete(db_book)
    db.commit()
    return None 


import uuid 
from datetime import datetime,timezone
from sqlalchemy import String,Text,Integer,Float,Numeric,Boolean,DateTime,Date,Time,ForeignKey,LargeBinary,Index,UniqueConstraint,func

from sqlalchemy.orm import Mapped,mapped_column,relationship

from database import Base 

class TimestampMixin: 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


















