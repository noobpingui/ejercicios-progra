import json

from app.extensions import redis_client


def get(key):
    value = redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)


def set(key, value, ttl=None):
    redis_client.set(key, json.dumps(value), ex=ttl)


def invalidate(key_or_pattern):
    if "*" in key_or_pattern:
        keys = redis_client.keys(key_or_pattern)
        if keys:
            redis_client.delete(*keys)
    else:
        redis_client.delete(key_or_pattern)
