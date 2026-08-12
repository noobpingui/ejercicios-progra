
from models.product import Product #SQLAlchemy model (The real table in Postgres)
from sqlalchemy.orm import Session #For the contructor
from sqlalchemy import select #Required to build SELECT queries

from schemas.product_schema import ProductSchema #The Pydantic schema. Basically, the 'shape' of the product from the 'outside'
from pydantic import TypeAdapter #Pydantic tool to validates/serializes lists of a scheme

import redis #To capture redis.exceptions.RedisError specifically
import logging #Standard python module to create logs instead of using print()


logger = logging.getLogger(__name__) #A logger with the file name in order to identify the source of the warning

CACHE_TTL = 300 #This is 5 min in seconds. The lifetime of a key in Redis. It's a security measure in case a validation fails

ALL_PRODUCTS_CACHE_KEY = "products:all" #Constant to keep this string in a single place in order to avoid typos if used in different methods

product_list_adapter = TypeAdapter(list[ProductSchema]) #BaseModel does not know how to handle a list of 'itself'(a schema) directly, hence
                                                        #TypeAdapter it's a specialized object that allows to work with lists of the scheme

class ProductRepository():
    def __init__(self, db: Session, redis_client): #The constructor receives the DB session and the Redis client through dependency injection
        self.db = db #SQLAlchemy session. (The real source of data)
        self.redis_client = redis_client #Redis client. (The cached data)


    def _cache_key(self, product_id: int): #Helper function to build the key 'product:{id}' in a single place and avoid manually repeating the f-string 
                                           #on each required method (To avoid typos)
        return f"product:{product_id}"
    
    #HELPERS for Redis
    def _cache_get(self, key: str): #To try reading the key from Redis (Cache Hit)
        try:
            return self.redis_client.get(key)
        except redis.exceptions.RedisError as error:
            logger.warning(f"Data could not be read from Redis (key='{key}'): {error}")  
            return None #Cache miss, the flow goes to Postgres as regular

    def _cache_set(self, key: str, value: str, ttl: int = CACHE_TTL): #To try writting on Redis 
        try:
            self.redis_client.setex(key, ttl, value)
        except redis.exceptions.RedisError as error:
            logger.warning(f"Data could not be written on Redis (key='{key}'): {error}") 

    def _cache_delete(self, key:str): #To try data invalidation on Redis
        try:
            self.redis_client.delete(key)
        except redis.exceptions.RedisError as error:
            logger.warning(f"Data could not be invalidated (key='{key}'): {error}") #If the invalidation fails, the commit on Progress has been already done anyway




    #CRUD
    
    #CREATE PRODUCT
    def create_product(self, product: Product):
        self.db.add(product) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(product) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        self._cache_delete(ALL_PRODUCTS_CACHE_KEY) #To invalidate the 'cached list' due to the list changed - (There's a new product)

        return ProductSchema.model_validate(product) #To turn the SQLAlchemy product into a product Schema and returns it

    #GET ALL PRODUCTS
    def get_all_products(self):

        cached = self._cache_get(ALL_PRODUCTS_CACHE_KEY) #Tries to get the 'cached list' (None if it does not exist or it's expired)

        #cache HIT = There was data cached
        if cached is not None:
            return product_list_adapter.validate_json(cached) #Builds the list of ProductSchema from the JSON cached

        #cache MISS: There was no data cached, hence, it's necessary to look for it in Postgres
        products = self.db.execute(select(Product)).scalars().all()

        schemas = [ProductSchema.model_validate(product) for product in products] #Turns each product into ProductSchema

        #To store the list that has been already serialized to JSON in Redis, with the expiration CACHE_TTL
        self._cache_set(ALL_PRODUCTS_CACHE_KEY, product_list_adapter.dump_json(schemas)) 

        return schemas #Returns the same list of ProductSchema that has been just cached

    #GET PRODUCT BY ID
    def get_product_by_id(self, product_id: int):

        cache_key = self._cache_key(product_id) #To build the specific key "Eg: (product:5)"

        cached = self._cache_get(cache_key) #Tries to brings the cached product

        #cache HIT = There was data cached
        if cached is not None:
            return ProductSchema.model_validate_json(cached) #Builds the ProductSchema from the JSON cached

        #cache MISS: There was no data cached, hence, it's necessary to look for it in Postgres
        product = self.db.get(Product, product_id) #db.get() look for the PK directly

        if product is None: #It does not exist in the DB
            return None #There's nothing to catch, hence, it returns None

        schema = ProductSchema.model_validate(product) #Turns the product found into a ProductSchema

        #To store the schema that has been already serialized to JSON in Redis, with the expiration CACHE_TTL
        self._cache_set(cache_key, schema.model_dump_json()) 
        
        return schema  #Returns the schema that has been just cached
    
    #GET PRODUCT BY NAME
    def get_product_by_name(self, name: str): #It's not necessary to cache this method since it main porpuse is to check for duplicates before creating a product
                                              #Further, the method requires the most updated data directly from the db, not a potenciatially aged data cached

        stmt = select(Product).where(Product.name == name)

        product = self.db.execute(stmt).scalars().first()

        return product


    #DELETE PRODUCT
    def delete_product(self, product_id: int):

        product = self.db.get(Product, product_id)
        self.db.delete(product)
        self.db.commit()

        self._cache_delete(self._cache_key(product_id)) #To invalidate the specific key, for example "product:5"
        self._cache_delete(ALL_PRODUCTS_CACHE_KEY) #To invalidate the entire list since it changed after the delete

        return None

    #UPDATE PRODUCT
    def update_product(self, product_id: int, name=None, price=None, quantity=None):

        product = self.db.get(Product, product_id)

        #Modifico la data si el campo que llega no es None
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if quantity is not None:
            product.quantity = quantity

        #Guardo los cambios realizados
        self.db.commit()

        #Sincronizo la data
        self.db.refresh(product)

        #To invalidate the specific key, for example "product:5". The data cached is old now
        self._cache_delete(self._cache_key(product_id))

        #To invalidate the entire list since it changed after the update
        self._cache_delete(ALL_PRODUCTS_CACHE_KEY)


        return ProductSchema.model_validate(product) #Returns the updated product as a ProductSchema
    
    