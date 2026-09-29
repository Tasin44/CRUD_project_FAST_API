import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

SQLALCHEMY_DATABASE_URL="sqlite:///./books.db"#❓ is it always remain same for db sqlite

# For PostgreSQL later, uncomment:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/booksdb"


engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
)


SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()
