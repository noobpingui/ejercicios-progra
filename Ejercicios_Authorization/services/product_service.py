

from models.product import Product
from repositories.product_repository import ProductRepository
from exceptions.product_exceptions import DuplicatedProductName, ProductNotExist



class ProductService():
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository


    def create_product(self, product: Product):
        
        existing_product = self.product_repository.get_product_by_name(product.name)
        if existing_product:
            raise DuplicatedProductName("A product with that name has been registered already")
        
        new_product = self.product_repository.create_product(product)

        return new_product

    def get_product_by_id(self, product_id: int):

        product = self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotExist(f"The product with the ID: {product_id} does not exist")
        
        return product
    
    def get_product_by_name(self, product_name: str):

        product = self.product_repository.get_product_by_name(product_name)
        if product is None:
            raise ProductNotExist(f"A product with that name has not been registered yet")
        
        return product
        
    def delete_product(self, product_id: int):

        product = self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotExist(f"The product with the ID: {product_id} does not exist")
        
        self.product_repository.delete_product(product.id)

        return None

    def update_product(self, product_id: int, name=None, price=None, quantity=None):

        product = self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotExist(f"The product with the ID: {product_id} does not exist")
        
        if name is not None:
            product.name = name

        if price is not None:
            product.price = price
        
        if quantity is not None:
            product.quantity = quantity

        updated_product = self.product_repository.update_product(product.id, product.name, product.price, product.quantity)

        return updated_product
    
