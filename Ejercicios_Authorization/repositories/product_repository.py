
from models.product import Product
from sqlalchemy.orm import Session
from sqlalchemy import select

class ProductRepository():
    def __init__(self, db: Session):
        self.db = db

    
    #CREATE PRODUCT
    def create_product(self, product: Product):
        self.db.add(product) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(product) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        return product

    #GET ALL PRODUCTS
    def get_all_products(self):
        #select(Product) -- contruye la query SELECT * FROM products
        #self.db.execute(...) -- ejecuta la query y devuelve un resultado crudo en filas
        #.scalars() -- convierte las filas en objetos Python(Product), en lugar de tuplas
        # .all() -- materializa todo en una lista 
        #El flujo es: query → ejecutar → convertir a objetos → lista
        products = self.db.execute(select(Product)).scalars().all()

        return products



    #GET PRODUCT BY ID
    def get_product_by_id(self, product_id: int):

        product = self.db.get(Product, product_id)
        
        return product
    
    #GET PRODUCT BY NAME
    def get_product_by_name(self, name: str):

        stmt = select(Product).where(Product.name == name)

        product = self.db.execute(stmt).scalars().first()

        return product


    #DELETE PRODUCT
    def delete_product(self, product_id: int):

        product = self.db.get(Product, product_id)
        self.db.delete(product)
        self.db.commit()

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
    
    