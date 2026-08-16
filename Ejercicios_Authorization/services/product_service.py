

from models.product import Product
from repositories.product_repository import ProductRepository
from exceptions.product_exceptions import DuplicatedProductName, ProductNotExists

from schemas.product_schema import ProductSchema #The Pydantic schema. Basically, the 'shape' of the product from the 'outside'
from pydantic import TypeAdapter #Pydantic tool to validates/serializes lists of a scheme

from redis_cache import RedisCache

ALL_PRODUCTS_CACHE_KEY = "products:all" #Constant to keep this string in a single place in order to avoid typos if used in different methods

product_list_adapter = TypeAdapter(list[ProductSchema]) #BaseModel does not know how to handle a list of 'itself'(a schema) directly, hence
                                                        #TypeAdapter it's a specialized object that allows to work with lists of the scheme
class ProductService():
    def __init__(self, product_repository: ProductRepository, redis_client):
        self.product_repository = product_repository
        self.cache = RedisCache(redis_client, prefix="product")

    #CREATE PRODUCT
    def create_product(self, product: Product):

        existing_product = self.product_repository.get_product_by_name(product.name)
        if existing_product:
            raise DuplicatedProductName("A product with that name has been registered already")

        new_product = self.product_repository.create_product(product)

        self.cache.delete(ALL_PRODUCTS_CACHE_KEY) #To invalidate the 'cached list' due to the list changed - (There's a new product)

        return ProductSchema.model_validate(new_product) #To turn the SQLAlchemy product into a product Schema and returns it

    #GET ALL PRODUCTS
    def get_all_products(self):

        cached = self.cache.get(ALL_PRODUCTS_CACHE_KEY) #Tries to get the 'cached list' (None if it does not exist or it's expired)

        #cache HIT = There was data cached
        if cached is not None:
            return product_list_adapter.validate_json(cached) #Builds the list of ProductSchema from the JSON cached

        #cache MISS: There was no data cached, hence, it's necessary to look for it in Postgres
        products = self.product_repository.get_all_products()

        schemas = [ProductSchema.model_validate(product) for product in products] #Turns each product into ProductSchema

        #To store the list that has been already serialized to JSON in Redis, with the expiration CACHE_TTL
        self.cache.set(ALL_PRODUCTS_CACHE_KEY, product_list_adapter.dump_json(schemas))

        return schemas #Returns the same list of ProductSchema that has been just cached

    #GET PRODUCT BY ID
    def get_product_by_id(self, product_id: int):

        cache_key = self.cache.key(product_id) #To build the specific key "Eg: (product:5)"

        cached = self.cache.get(cache_key) #Tries to bring the cached product

        #cache HIT = There was data cached
        if cached is not None:
            return ProductSchema.model_validate_json(cached) #Builds the ProductSchema from the JSON cached

        #cache MISS: There was no data cached, hence, it's necessary to look for it in Postgres
        product = self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotExists(f"The product with the ID: {product_id} does not exist")

        schema = ProductSchema.model_validate(product) #Turns the product found into a ProductSchema

        #To store the schema that has been already serialized to JSON in Redis, with the expiration CACHE_TTL
        self.cache.set(cache_key, schema.model_dump_json())

        return schema #Returns the schema that has been just cached

    #GET PRODUCT BY NAME
    def get_product_by_name(self, product_name: str): #It's not necessary to cache this method since its main purpose is to check for duplicates before creating a product
                                                       #Further, the method requires the most updated data directly from the db, not a potentially aged data cached

        product = self.product_repository.get_product_by_name(product_name)
        if product is None:
            raise ProductNotExists(f"A product with that name has not been registered yet")

        return product

    #DELETE PRODUCT
    def delete_product(self, product_id: int):

        product = self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotExists(f"The product with the ID: {product_id} does not exist")

        self.product_repository.delete_product(product.id)

        self.cache.delete(self.cache.key(product_id)) #To invalidate the specific key, for example "product:5"
        self.cache.delete(ALL_PRODUCTS_CACHE_KEY) #To invalidate the entire list since it changed after the delete

        return None

    #UPDATE PRODUCT
    def update_product(self, product_id: int, name=None, price=None, quantity=None):

        product = self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotExists(f"The product with the ID: {product_id} does not exist")

        if name is not None:
            product.name = name

        if price is not None:
            product.price = price

        if quantity is not None:
            product.quantity = quantity

        updated_product = self.product_repository.update_product(product.id, product.name, product.price, product.quantity)

        self.cache.delete(self.cache.key(product_id)) #To invalidate the specific key, for example "product:5". The data cached is old now
        self.cache.delete(ALL_PRODUCTS_CACHE_KEY) #To invalidate the entire list since it changed after the update

        return ProductSchema.model_validate(updated_product) #Returns the updated product as a ProductSchema
