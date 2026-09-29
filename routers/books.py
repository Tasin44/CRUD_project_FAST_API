#routers/books.py — APIRouter (like Views + URLs combined)

from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List

import models 
import schemas 
from datetime import get_db 

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.post("/",response_model=schemas.BookResponse,status_code=status.HTTP_201_CREATED)
def create_book(book:schemas.BookCreate,db:Session=Depends(get_db)):
  db_book=models.Book(**book.model_dump())
  db.add(db_book)
  db.commit()
  db.refresh(db_book)
  return db_book














