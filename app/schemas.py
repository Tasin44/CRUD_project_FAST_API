#schemas.py — Pydantic Schemas (like DRF Serializers)


from pydantic import BaseModel,Field
from typing import Optional

# BaseModel → base class for Pydantic schemas.
# Field() → lets you add validation rules.
'''
Django analogy: In DRF, one BookSerializer handles everything. Here, you have separate schemas. BookCreate is like the write serializer, BookResponse is like the read serializer, and BookUpdate handles partial updates.

The from_attributes = True (Pydantic v2) is equivalent to DRF's ModelSerializer automatically reading from model instances.
'''

# Base schema — shared fields
class BookBase(BaseModel): # like drf class BookSerializer(serializers.Serializer):
    title:str=Field(...,min_length=1,max_length=200)#
    '''
title: str = Field(...)

... means:
title is required.
You cannot replace ... with more dots or fewer dots, so I've to use exactly 3 dots

------You can also write:

title: str

and it is already required.
    '''
    author:str=Field(...,min_length=1,max_length=100)
    price:float=Field(...,gt=0)
    in_stock:bool=True

# Create schema — input for POST
#❓why I've not written the whole class here 
'''
BookCreate automatically copies all the fields (title, author, price, in_stock) from BookBase. You write pass because you don't need to add or change anything. Keeping a separate BookCreate name is a best practice so you can easily add specific creation logic later if needed without breaking other parts of your app.


Why create it at all then, instead of using BookBase directly?

Because later you'll likely want to change BookCreate without affecting BookBase. 
For example:

class BookCreate(BookBase):
    # Add a field only for creation, like a secret admin note
    internal_note: Optional[str] = None

Or if BookBase had an id and you don't want clients sending id on create, BookCreate can override it.
'''
class BookCreate(BookBase):
    pass

# Update schema — all fields optional for PATCH
class BookUpdate(BaseModel):
    title:Optional[str]=Field(None,min_length=1,max_length=200)
    author:Optional[str]=Field(None,min_length=1,max_length=100)
    price:Optional[float]=Field(None,gt=0)
    in_stock:Optional[bool]=None

# Read schema — output, includes the ID
class BookResponse(BookBase):
    id:int #❓why id written here in this way, why not like title and author written on the above
    '''
    Why id: int doesn't use Field(...)?

        Because you don't need any special validation rule.

        This:

            id: int

        means:

        id must be an integer and is required.

        You could write:

            id: int = Field(...)

        but there's no need.
        So final response looks like:

        {
            "id": 1,
            "title": "Django Book",
            "author": "John",
            "price": 20,
            "in_stock": true
        }
    '''

    class Config:
        from_attributes = True # Allows creating from SQLAlchemy model objects
'''
Your SQLAlchemy gives you:

db_book

which is a Python object:

Book object
    ↓
id
title
author
price
in_stock

But BookResponse is a Pydantic model.

from_attributes=True tells Pydantic:

SQLAlchemy object
       ↓
read its attributes
       ↓
BookResponse
       ↓
JSON

This is somewhat similar to DRF's ability to serialize model instances.


Reason behind the from_attributes = True: 

it teaches Pydantic how to read SQLAlchemy objects.

By default, Pydantic schemas (like BookResponse) only know how to read standard Python dictionaries.

If you give a normal Pydantic schema a dictionary, it looks up data like this:
book["title"]

But your database gives you back a SQLAlchemy Model, which is a Python object. Objects hold their data in attributes, not dictionary keys:
book.title

If you try to return a SQLAlchemy object without that Config class, Pydantic gets confused and throws an error because it can't find book["title"].

Adding from_attributes = True tells Pydantic:

    "If I hand you an object instead of a dictionary, don't panic. Just read the data using dot notation (attribute access) instead."

Why is it only on BookResponse?

Because BookResponse is your output schema.

    The user sends JSON (FastAPI converts this to a dictionary for BookCreate).

    You save it to the database (it becomes a SQLAlchemy object).

    You want to send that object back to the user as JSON (BookResponse needs to read the SQLAlchemy object).

(Note: In older FastAPI/Pydantic tutorials, you will often see this written as orm_mode = True. from_attributes = True is simply the updated name for the exact same feature.)
'''






