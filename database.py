from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:postgres@localhost:5432/EnCoderTest' 

'''Making the connection into the local postgres database. Using the username and the password for postgres, the route,
the port (which default is 5432) and the name of the database'''

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

'''Create the session. Setting autoflush to false, so we keep the control over the changes.
autocommit is false so we can make multiple operation and step by step and rollback if its needed'''

Base = declarative_base()