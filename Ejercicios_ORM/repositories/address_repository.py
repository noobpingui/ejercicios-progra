from sqlalchemy.orm import Session
from sqlalchemy import select
from models.address import Address
from exceptions.address_exceptions import AddressNotFound

class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    #Create Address:
    def create_address(self, address: Address):
        self.db.add(address) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(address) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        return address
    
    #Get Address by Id:
    def get_address_by_id(self, address_id: int):
        
        address = self.db.get(Address, address_id)

        if address is None:
            raise AddressNotFound(f"The Address with id:{address_id} was not found")

        return address
    
    #Update Adress:
    def update_address(self, address_id: int, province=None, city=None, street=None, 
                       additional_directions=None, user_id=None):
        
        #Obtengo el address por id
        address = self.get_address_by_id(address_id)
        
        #Modifico la data si el campo que llega no es None
        if province is not None:
            address.province = province
        if city is not None:
            address.city = city
        if street is not None:
            address.street = street
        if additional_directions is not None:
            address.additional_directions = additional_directions
        if user_id is not None:
            address.user_id = user_id

        #Guardo los cambios realizados
        self.db.commit()

        #Sincronizo la data
        self.db.refresh(address)

        return address
    
    #Delete Address:
    def delete_address(self, address_id: int):

        #Obtengo el address por id
        address = self.get_address_by_id(address_id)

        #Borro el address
        self.db.delete(address)

        #Guardo los cambios realizados
        self.db.commit()

        return address
    
    #Get all addresses:
    def get_all_addresses(self):
        
        #select(Address) -- contruye la query SELECT * FROM addresses
        #self.db.execute(...) -- ejecuta la query y devuelve un resultado crudo en filas
        #.scalars() -- convierte las filas en objetos Python(Address), en lugar de tuplas
        # .all() -- materializa todo en una lista 
        #El flujo es: query → ejecutar → convertir a objetos → lista
        
        addresses = self.db.execute(select(Address)).scalars().all()

        return addresses
    
