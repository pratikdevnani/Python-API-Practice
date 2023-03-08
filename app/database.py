from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# basically give the location of the postgres location and the database
SQLALCHEMY_DATABASE_URL = 'postgres://postgres:Monster@0255@localhost/fastapi'

# we need an engine to make a connection with the Database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# we need a base so that each python model can import
Base = declarative_base()