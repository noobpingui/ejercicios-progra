

from models.invoice import Invoice
from sqlalchemy.orm import Session
from sqlalchemy import select


class InvoiceRepository():
    def __init__(self, db: Session):
        self.db = db

    #CREATE INVOICE
    def create_invoice(self, invoice: Invoice):
        self.db.add(invoice) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(invoice) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        return invoice
    

    #GET ALL Invoices
    def get_all_invoices_by_user(self, user_id):
        #select(Invoice) -- contruye la query SELECT
        #where -- filtra por user_id 
        #self.db.execute(...) -- ejecuta la query y devuelve un resultado crudo en filas
        #.scalars() -- convierte las filas en objetos Python(User), en lugar de tuplas
        # .all() -- materializa todo en una lista 
        #El flujo es: query → ejecutar → convertir a objetos → lista

        invoices = self.db.execute(
        (select(Invoice)).where(Invoice.user_id == user_id)
        ).scalars().all()

        return invoices

    #GET INVOICE BY ID
    def get_invoice_by_id(self, invoice_id: int):

        invoice = self.db.get(Invoice, invoice_id)
        
        return invoice
    
    #DELETE INVOICE
    def delete_invoice(self, invoice_id: int):

        invoice = self.db.get(Invoice, invoice_id)
        self.db.delete(invoice)
        self.db.commit()

        return None
    
    #UPDATE INVOICE
    def update_invoice(self, invoice_id: int, quantity=None, total_price=None):

        invoice = self.db.get(Invoice, invoice_id)

        #Modifico la data si el campo que llega no es None
        if quantity is not None:
            invoice.quantity = quantity
        if total_price is not None:
            invoice.total_price = total_price
        
        #Guardo los cambios realizados
        self.db.commit()

        #Sincronizo la data
        self.db.refresh(invoice)

        return invoice
    