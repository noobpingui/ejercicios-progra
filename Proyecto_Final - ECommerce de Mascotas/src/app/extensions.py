import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from app.config import Config

Base = declarative_base()

engine = create_engine(Config.DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

redis_client = redis.from_url(Config.REDIS_URL)
