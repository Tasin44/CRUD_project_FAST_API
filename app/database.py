import sqlalchemy#Imports the core SQLAlchemy library, the standard Python tool for interacting with databases.
from sqlalchemy import create_engine#Imports the function that acts as the core "translator" and connection point between Python and your database.
from sqlalchemy.orm import sessionmaker,declarative_base#Imports tools to manage database connections (sessionmaker) and map Python classes to database tables (declarative_base).

SQLALCHEMY_DATABASE_URL="sqlite:///./books.db"#❓ is it always remain same for db sqlite
'''
No, it does not always remain exactly the same. The sqlite:/// part is required for SQLite, but ./books.db is just the file path and name. If you wanted to name your database users.db in a different folder, it would change (e.g., sqlite:///./data/users.db).
'''

# For PostgreSQL later, uncomment:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/booksdb"


engine=create_engine(#Actually creates the connection point using the URL defined above.
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False} # ONLY required for SQLite
)
'''
connect_args={"check_same_thread": False}

Specific to SQLite. SQLite normally blocks multiple threads from sharing a single connection. FastAPI runs multiple threads to handle simultaneous web requests, so this setting tells SQLite to allow it.
'''


SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
'''
Creates a "factory" that produces temporary database sessions.

    autocommit=False: Requires you to manually save (commit()) changes, preventing accidental saves.

    autoflush=False: Prevents SQLAlchemy from prematurely sending data to the database before you are ready.

    bind=engine: Connects these sessions to the engine we just created.
'''
Base=declarative_base()
'''
Creates a base class. When you create database tables later (like a Book or User model), they will inherit from this Base so SQLAlchemy knows they represent tables.
'''

# Dependency — this is FastAPI's way of injecting DB sessions into routes
'''
This is your DATABASES setting + connection management, combined. 
The get_db function is a dependency that FastAPI will automatically call 
for any route that needs a database session.
'''
def get_db():
    db=SessionLocal()#Creates a fresh, new database session for the current request.
    try:
        yield db #Pauses the function and hands the db session to the FastAPI route to use.
    finally:#Ensures that no matter what happens (even if the route crashes), the database connection is safely closed when the request is finished
        db.close()
