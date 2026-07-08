
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#Models

from models.base import Base
from models.user import User

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

#SessionMaker
SessionLocal = sessionmaker(bind=engine)