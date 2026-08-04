
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

#Models

from models.base import Base

# SQLAlchemy only knows about a model after its class has been imported
# By importing the models, this trigger the registration of the model before create_all runs.
from models.user import User
from models.product import Product
from models.invoice import Invoice

load_dotenv()

DB_URI = os.getenv('DATABASE_URL')
engine = create_engine(DB_URI, echo=True)

try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()

except Exception as e:
    print("Connection failed:", e)

Base.metadata.create_all(engine)



# scoped_session wraps sessionmaker in an object whose job is: "when someone asks me for a session, 
# look up whether the current context (by default, current thread) already has one; 
# if yes, return that same one; if no, create one, store it, and return it.

#Session
Session = scoped_session(
    sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )
)

