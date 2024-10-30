from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# this is the path to the database file
SQLALCHEMY_DATABASE_URI = 'sqlite:///./todosapp.db'

# here we create the engine, this means we are connecting to the database,
# we also set the connect_args to {"check_same_thread": False} to avoid threading issues
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

# here we create the session local, this is the session that we will use to interact with the database
# we set autocommit to False and autoflush to False ,to avoid autocommiting and autoflushing
# we also bind the session to the engine
# this means that the session will use the engine to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# here we create the base class for our models
# this is the class that our models will inherit from
# this class will contain the metadata of the database
Base = declarative_base()
