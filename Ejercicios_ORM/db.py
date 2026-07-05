from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#Models
from models.base import Base
from models.user import User
from models.car import Car
from models.address import Address


# dialect+driver://...
# - dialect = el tipo de DB (postgresql)
# - driver = la libreria que hace la conexion real (psycopg2)
# Normalmente psycopg2 es el default, por eso funciona sin ponerlo.

load_dotenv()

DB_URI = os.getenv('DB_URI')
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

