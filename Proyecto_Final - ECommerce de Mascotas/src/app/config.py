import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.environ.get("DATABASE_URL")
    REDIS_URL = os.environ.get("REDIS_URL")

    JWT_PRIVATE_KEY_PATH = os.environ.get("JWT_PRIVATE_KEY_PATH")
    JWT_PUBLIC_KEY_PATH = os.environ.get("JWT_PUBLIC_KEY_PATH")
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "RS256")
    JWT_EXP_MINUTES = int(os.environ.get("JWT_EXP_MINUTES", "30"))

    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
