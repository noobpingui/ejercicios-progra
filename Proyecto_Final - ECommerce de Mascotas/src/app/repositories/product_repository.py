from app.models.product import Product, ProductStatusEnum


class ProductRepository:
    def __init__(self, session):
        self.session = session

    def create(self, name, description, price, stock):
        product = Product(name=name, description=description, price=price, stock=stock)
        self.session.add(product)
        return product

    def get_by_id(self, product_id):
        return self.session.query(Product).filter_by(product_id=product_id).first()

    def get_for_update(self, product_id):
        # SELECT ... FOR UPDATE: bloquea la fila hasta que la transacción actual
        # termine (commit/rollback). Uso exclusivo de operaciones que van a leer
        # y luego mutar el stock dentro de la misma transacción (ej. checkout) —
        # get_by_id sigue siendo el método normal para lecturas.
        return (
            self.session.query(Product)
            .filter_by(product_id=product_id)
            .with_for_update()
            .first()
        )

    def list_active(self):
        return self.session.query(Product).filter_by(status=ProductStatusEnum.active).all()

    def reduce_stock(self, product, quantity):
        product.stock -= quantity
        return product

    def restore_stock(self, product, quantity):
        product.stock += quantity
        return product
