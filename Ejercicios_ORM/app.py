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

#Exceptions
from exceptions.user_exceptions import UserNotFound
from exceptions.car_exceptions import CarNotFound, RelatedUserIdNotFound
from exceptions.address_exceptions import AddressNotFound




#Para crear un session
session = SessionLocal()

#Sessions:
user_repository = UserRepository(session)
car_repository = CarRepository(session)
address_repository = AddressRepository(session)

#---------------------------------------------------------

def tests_for_users():
    
    try:
        new_user = User(name="Goku", email="kakarot@example.com", status=UserStatus.active)

        print(user_repository.create_user(new_user))
        #print(user_repository.get_user_by_id())
        #print(user_repository.update_user(2, email="george@example.com"))
        #print(user_repository.get_all_users())
        #print(user_repository.delete_user())
        
    except UserNotFound as error:
        print(error)

    
def tests_for_cars():

    try:
        new_car = Car(brand="Tesla", model="S", year=2019, status=CarStatus.available)

        #print(car_repository.create_car(new_car))
        #print(car_repository.get_car_by_id())
        #print(car_repository.update_car(1, status='available'))
        #print(car_repository.get_all_cars())
        #print(car_repository.to_relate_car_to_user(14,7))
        print(car_repository.delete_car(19))
        
    except CarNotFound as error:
        print (error)
    except RelatedUserIdNotFound as error:
        print (error)

    
def tests_for_addresses():

    try:
        new_address = Address(province="San Jose", city="Curridabat", street='Nova', additional_directions='Cerca', user_id=6)

        #print(address_repository.create_address(new_address))
        #print(address_repository.get_address_by_id())
        #print(address_repository.update_address(4, street='Tamarindo', city='Liberia', user_id=5))
        #print(address_repository.get_all_addresses())
        #print(address_repository.delete_address(4))

    except AddressNotFound as error:
        print(error)


try:
#--------Pruebas para Users--------
    tests_for_users()
#--------Pruebas para Cars--------
    tests_for_cars()
#--------Pruebas para Addresses---------
    tests_for_addresses()

finally:
    session.close()




















#Pruebas despues de implementar relation()

# selected_user = user_repository.get_user_by_id(1)
# selected_car = car_repository.get_car_by_id(4)
# selected_address = address_repository.get_address_by_id(1)

#selected_user.cars.append(selected_car) #Puedo acceder a la lista de cars que pertenece a selected_user y agregar selected_car
#session.add(selected_car)
#session.commit()

#print(selected_user.cars) #Acceder todos los cars de el user 'selected_user'
#print(selected_car.user.name) #Acceder el nombre de el user que tiene asignado el 'selected_car'
#print(selected_car.user.email) #Acceder el email de el user que tiene asignado el 'selected_car'
#print(selected_user.addresses) #Acceder a todas las direcciones de el user 'selected_user'
#print(selected_address.user.name) #Acceder a el nombre de el user que tiene asignada la 'selected_address'