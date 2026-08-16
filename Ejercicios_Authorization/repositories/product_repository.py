
from models.product import Product #SQLAlchemy model (The real table in Postgres)
from sqlalchemy.orm import Session #For the contructor
from sqlalchemy import select #Required to build SELECT queries

from sqlalchemy.exc import IntegrityError #Required to 'catch' the error related to the DB, in this particular case when trying to delete a product that is related to the invoice / So we can show a 'friendly' message to the user instead of an ugly error window or even worse, the app stops working
from exceptions.product_exceptions import ProductInUse 

class ProductRepository():
    def __init__(self, db: Session): #The constructor receives the DB session
        self.db = db #SQLAlchemy session. (The real source of data)
        
    #CRUD
    
    #CREATE PRODUCT
    def create_product(self, product: Product):
        self.db.add(product) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(product) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        return product

    #GET ALL PRODUCTS
    def get_all_products(self):

        products = self.db.execute(select(Product)).scalars().all()

        return products
    
    #GET PRODUCT BY ID
    def get_product_by_id(self, product_id: int):

        product = self.db.get(Product, product_id) #db.get() look for the PK directly

        if product is None: #It does not exist in the DB
            return None 
    
        return product
    
    #GET PRODUCT BY NAME
    def get_product_by_name(self, name: str):

        stmt = select(Product).where(Product.name == name)

        product = self.db.execute(stmt).scalars().first()

        return product


    #DELETE PRODUCT
    def delete_product(self, product_id: int):

        product = self.db.get(Product, product_id)
        try:
            self.db.delete(product)
            self.db.commit()

        except IntegrityError:
            self.db.rollback() #Required since the commit was rejected by Postgress due to the FK, hence, the rollback is required to 'clear' the session and set it fresh to use
            raise ProductInUse(f"The product with the ID: {product_id} cannot be deleted because it has associated invoices")

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

        return product
    