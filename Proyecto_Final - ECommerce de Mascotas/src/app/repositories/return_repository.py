from sqlalchemy import func

from app.models.return_ import Return, ReturnItem


class ReturnRepository:
    def __init__(self, session):
        self.session = session

    def create(self, invoice_number):
        return_ = Return(invoice_number=invoice_number)
        self.session.add(return_)
        return return_

    def add_item(self, return_, invoice_item_id, quantity):
        item = ReturnItem(invoice_item_id=invoice_item_id, quantity=quantity)
        return_.items.append(item)
        return item

    def get_total_returned_quantity(self, invoice_item_id):
        # Suma todas las devoluciones previas (de cualquier Return) de esa
        # línea de factura
        return (
            self.session.query(func.coalesce(func.sum(ReturnItem.quantity), 0))
            .filter_by(invoice_item_id=invoice_item_id)
            .scalar()
        )
