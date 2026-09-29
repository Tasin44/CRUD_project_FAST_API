#schemas.py — Pydantic Schemas (like DRF Serializers)


from pydantic import BaseModel,Field
from typing import Optional

'''
Django analogy: In DRF, one BookSerializer handles everything. Here, you have separate schemas. BookCreate is like the write serializer, BookResponse is like the read serializer, and BookUpdate handles partial updates.

The from_attributes = True (Pydantic v2) is equivalent to DRF's ModelSerializer automatically reading from model instances.
'''

# Base schema — shared fields
class BookBase(BaseModel):
    title:str=Field(...,min_length=1,max_length=200)#❓why ... used here, is it necessary to use 3 dot or I can use more or less
    author:str=Field(...,min_length=1,max_length=100)
    price:float=Field(...,gt=0)
    in_stock:bool=True

# Create schema — input for POST
#❓why I've not written the whole class here 
class BookCreate(BookBase):
    pass

# Update schema — all fields optional for PATCH
class BookUpdate(BaseModel):
    title:Optional[str]=Field(None,min_length=1,max_length=200)
    author:Optional[str]=Field(None,min_length=1,max_length=100)
    price=Optional[float]=Field(None,gt=0)
    in_stock:Optional[bool]=None

# Read schema — output, includes the ID
class BookResponse(BookBase):
    id:int #❓why id written here in this way, why not like title and author written on the above

    class Config:
        from_attributes = True # Allows creating from SQLAlchemy model objects
