from app.models.invoice import Invoice, InvoiceItem


class InvoiceRepository:
    def __init__(self, session):
        self.session = session

    def create(
        self,
        user_id,
        billing_street,
        billing_city,
        billing_postal_code,
        billing_country,
        payment_method,
    ):
        invoice = Invoice(
            user_id=user_id,
            billing_street=billing_street,
            billing_city=billing_city,
            billing_postal_code=billing_postal_code,
            billing_country=billing_country,
            payment_method=payment_method,
        )
        self.session.add(invoice)
        return invoice

    def add_item(self, invoice, product_id, quantity, price_at_purchase):
        # Se agrega vía la relacion (no seteando invoice_number a mano): SQLAlchemy
        # resuelve la FK sola al hacer flush, sin necesitar que invoice.invoice_number
        # ya este poblado en este punto
        item = InvoiceItem(product_id=product_id, quantity=quantity, price_at_purchase=price_at_purchase)
        invoice.items.append(item)
        return item

    def get_by_number(self, invoice_number):
        return self.session.query(Invoice).filter_by(invoice_number=invoice_number).first()

    def list_by_user(self, user_id):
        return self.session.query(Invoice).filter_by(user_id=user_id).all()

    def list_all(self):
        return self.session.query(Invoice).all()

    def get_item_for_update(self, invoice_number, invoice_item_id):
        # Filtra por invoice_number Y invoice_item_id en la misma query: si el
        # item no existe O existe pero pertenece a otra factura, el resultado es
        # el mismo None — mismo patron que get_owned_cart.
        # SELECT ... FOR UPDATE bloquea la fila para cerrar la condición de
        # carrera entre dos devoluciones concurrentes sobre la misma línea
        return (
            self.session.query(InvoiceItem)
            .filter_by(invoice_item_id=invoice_item_id, invoice_number=invoice_number)
            .with_for_update()
            .first()
        )
