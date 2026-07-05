from db import SessionLocal

#Users
from repositories.user_repository import UserRepository
from models.user import User, UserStatus

#Cars
from repositories.car_repository import CarRepository
from models.car import Car, CarStatus

#Address
from repositories.address_repository import AddressRepository
from models.address import Address


#Para crear un session
session = SessionLocal()


#--------Pruebas para Users--------
user_repository = UserRepository(session)
new_user = User(name="Panchito", email="panchito@example.com", status=UserStatus.active)

#CRUD User -- Completo

#user_repository.create_user(new_user)
#result = user_repository.get_user_by_id(2)
#result = user_repository.update_user(2, email="george@example.com")
#result = user_repository.get_all_users()
#print (result)
#user_repository.delete_user(2)


#--------Pruebas para Cars--------
car_repository = CarRepository(session)
new_car = Car(brand="Mazda", model="Miata", year=2003, status=CarStatus.available)

#CRUD Car -- Completo

#car_repository.create_car(new_car)
#result = car_repository.get_car_by_id(2)
#result = car_repository.update_car(2, status='available')
#result = car_repository.get_all_cars()
#result = car_repository.to_relate_car_to_user(3,1)
#print (result)
#car_repository.delete_car(2)



#Pruebas para Addresses
address_repository = AddressRepository(session)
new_address = Address(province="Guanacaste", city="Santa Cruz", street='Samara', additional_directions='Contiguo a mirador la Lapa', user_id=4)

#CRUD Address -- Completo

#address_repository.create_address(new_address)
#result = address_repository.get_address_by_id(2)
#result = address_repository.update_address(3, street='Tamarindo', city='Liberia', user_id=5)
#result = address_repository.get_all_addresses()
#print(result)
#address_repository.delete_address(4)
