#SQLAlchemy Models (like Django's models.py)
from sqlalchemy import null
from sqlalchemy import Column
from sqlalchemy import column,Integer,String,Float,Boolean
from database import Base

'''
Django analogy: This is exactly like a Django model, but you use Column(...) instead of Django's field classes, and Base instead of models.Model
'''
class Book(Base):
    __tablename__="books"

    id = Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True,nullable=False)
    author=Column(String,nullable=False)
    price=Column(Float,nullable=False)
    in_stock=Column(Boolean,default=True)