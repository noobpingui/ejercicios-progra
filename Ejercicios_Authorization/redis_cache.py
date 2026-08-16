
import redis #To capture redis.exceptions.RedisError specifically
import logging #Standard python module to create logs instead of using print()


logger = logging.getLogger(__name__) #A logger with the file name in order to identify the source of the warning

DEFAULT_TTL = 300 #This is 5 min in seconds. The lifetime of a key in Redis. It's a security measure in case a validation fails

class RedisCache:
    def __init__(self, redis_client, prefix: str, ttl: int = DEFAULT_TTL):
        self.redis_client = redis_client
        self.prefix = prefix #(For product, user, invoice, etc)
        self.ttl = ttl

    #Helper function to build a key for example: 'product:{id}' in a single place and avoid manually repeating the f-string
    #on each required method (To avoid typos) / Replaces the old method _cache_key
    def key(self, identifier): 
        return f"{self.prefix}:{identifier}" 

    def get(self, key): #Replaces the old method _cache_get / #To try reading the key from Redis (Cache Hit)
        try:
            return self.redis_client.get(key)

        except redis.exceptions.RedisError as error:
            logger.warning(f"Data could not be read from Redis (key='{key}'): {error}")
            return None

    def set(self, key, value, ttl: int = None): #Replaces the old method _cache_set / #To try writing on Redis
        try:
            if ttl is None or ttl <= 0: #Si no se pasa un ttl especifico o es menor/igual a 0, entonces se utuliza el default de la instancia
                ttl = self.ttl

            return self.redis_client.setex(key, ttl, value)

        except redis.exceptions.RedisError as error:
            logger.warning(f"Data could not be written to Redis (key='{key}'): {error}")

    def delete(self,key): #Replaces the old method _cache_delete / To try data invalidation on Redis
        try:
            self.redis_client.delete(key)

        except redis.exceptions.RedisError as error:
            logger.warning(f"Data could not be invalidated (key='{key}'): {error}")

