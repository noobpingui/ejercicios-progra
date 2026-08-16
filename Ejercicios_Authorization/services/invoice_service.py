
from models.invoice import Invoice
from repositories.invoice_repository import InvoiceRepository
from services.product_service import ProductService

from exceptions.product_exceptions import ProductNotExists, InsufficientStock

from exceptions.invoice_exceptions import InvoiceNotExists

class InvoiceService():
    def __init__(self, invoice_repository: InvoiceRepository, product_service: ProductService):
          self.invoice_repository = invoice_repository
          self.product_service = product_service

    def purchase_product(self, user_id: int, product_id: int, quantity: int):

        product = self.product_service.get_product_by_id(product_id)
        if product is None:
            raise ProductNotExists(f"The product with the ID: {product_id} does not exist")

        if quantity > product.quantity:
            raise InsufficientStock(f"Not enough stock. Available: {product.quantity}, requested: {quantity}")

        total_price = product.price * quantity

        new_invoice = Invoice(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price
        )

        invoice = self.invoice_repository.create_invoice(new_invoice)

        #To reduce product stock when a purchase is completed
        self.product_service.update_product(product_id, quantity=product.quantity - quantity)

        return invoice

    def get_invoices_by_user(self, user_id: int):

        invoices = self.invoice_repository.get_all_invoices_by_user(user_id)

        return invoices

    def delete_invoice(self, invoice_id: int):

        invoice = self.invoice_repository.get_invoice_by_id(invoice_id)
        if invoice is None:
            raise InvoiceNotExists(f"The invoice with the ID: {invoice_id} does not exist")

        self.invoice_repository.delete_invoice(invoice_id)

        return None

    def update_invoice(self, invoice_id: int, quantity=None, total_price=None):

        invoice = self.invoice_repository.get_invoice_by_id(invoice_id)
        if invoice is None:
            raise InvoiceNotExists(f"The invoice with the ID: {invoice_id} does not exist")

        updated_invoice = self.invoice_repository.update_invoice(invoice_id, quantity, total_price)

        return updated_invoice