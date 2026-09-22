from app.models.cart import Cart, CartItem, CartStatusEnum


class CartRepository:
    def __init__(self, session):
        self.session = session

    def create(self, user_id):
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        return cart

    def get_owned_cart(self, cart_id, user_id):
        return self.session.query(Cart).filter_by(cart_id=cart_id, user_id=user_id).first()

    def get_item(self, cart_id, cart_item_id):
        return (
            self.session.query(CartItem)
            .filter_by(cart_item_id=cart_item_id, cart_id=cart_id)
            .first()
        )

    def add_item(self, cart_id, product_id, quantity):
        item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self.session.add(item)
        return item

    def update_item_quantity(self, item, quantity):
        item.quantity = quantity
        return item

    def remove_item(self, item):
        self.session.delete(item)

    def list_pending_by_user(self, user_id):
        return (
            self.session.query(Cart)
            .filter_by(user_id=user_id, status=CartStatusEnum.pending)
            .all()
        )
