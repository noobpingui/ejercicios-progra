import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')

#decode_responses helps us to automaticaly convert the data returned from raw bytes -(b'vallue')- into Python strings -(value)-
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

try:
    redis_client.ping()
    print("Redis connection successful")
except Exception as e:
    print("Redis connection failed", e)


#redis uses its own connection pool, hence it is thread-safe, unlike SQLAlchemy that requires to implement a scoped_session.
#In other words, you can use a global instance for the entire app. It's not a single ConnectionPerRequest.



