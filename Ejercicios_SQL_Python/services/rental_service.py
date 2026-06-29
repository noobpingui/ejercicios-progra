
# El Service tiene métodos “de negocio”, el Repository tiene métodos “de datos”

# Service - Responsable de:

# - Crear rental
# - Aplicar reglas de negocio

from repositories.rental_repository import RentalRepository
from repositories.user_repository import UserRepository
from repositories.car_repository import CarRepository

from exceptions.rental_exceptions import UserNotExists, UserNotActive, UserIsDelinquent, CarNotExists, CarNotAvailable, RentalNotFound, RentalNotActive

from models.rental import RentalCreate, RentalStatus
from models.car import CarStatus


# Para los filters:
# ALLOWED_FILTERS define que columnas se permiten como filtro. El dict comprehension recorre los filtros que llegaron
# del request y solo conserva los que estan en esa lista — descartando cualquier key invalida o maliciosa. El dict
# limpio se pasa al repository que construye el SQL dinamicamente.
ALLOWED_FILTERS = {"id", "user_id", "car_id", "rental_date", "status"}

class RentalService():
    def __init__(self, rental_repository: RentalRepository, user_repository: UserRepository, car_repository: CarRepository):
        self.rental_repository = rental_repository
        self.user_repository = user_repository
        self.car_repository = car_repository
    

    #Required user validations to create a rent
    def _user_exists(self, user_id: int):
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            raise UserNotExists("The user does not exist")
        
        return existing_user
        
    def _user_status(self, user: dict):
        if user['status'] != 'active':
            raise UserNotActive("The user is not active")

    def _user_is_delinquent(self, user: dict):
        if user['is_delinquent'] != False:
            raise UserIsDelinquent("The user has been flagged as delinquent")
        
    #Required car validations to create a rent
    def _car_exists(self, car_id: int):
        existing_car = self.car_repository.get_car_by_id(car_id)
        if not existing_car:
            raise CarNotExists("The car does not exist")
        
        return existing_car
        
    def _car_status(self, car: dict):
        if car['status'] != 'available':
            raise CarNotAvailable("The car is not available")
        
    #Required validations to complete a rental
    def _rental_not_found(self, rental_id: int):
        existing_rental = self.rental_repository.get_rental_by_id(rental_id)
        if not existing_rental:
            raise RentalNotFound(f"The rental with the ID:{rental_id} does not exist")
        
        return existing_rental
    
    def _rental_not_active(self, rental: dict):
        if rental['status'] != 'active':
            raise RentalNotActive(f"This rental has been completed already")
    
    #Method to create a rental
    def create_rental(self, rental: RentalCreate):

        #------Validations related to user------
        #User exists validation
        user = self._user_exists(rental.user_id)
        
        #User status active validation
        self._user_status(user)

        #User is not delinquent validation
        self._user_is_delinquent(user)

        #------Validations related to Car------
        #Car exists validation
        car = self._car_exists(rental.car_id)

        #Car status available validation
        self._car_status(car)

        #Rental creation
        created_rental = self.rental_repository.create_rental(rental)

        self.car_repository.update_car_status(CarStatus.rented,rental.car_id)

        return created_rental
    
    def complete_rental(self, rental_id, status: RentalStatus):
        rental = self._rental_not_found(rental_id)
        self._rental_not_active(rental)

        rental_completed = self.rental_repository.complete_rental(status, rental_id)
        self.car_repository.update_car_status(CarStatus.available, rental['car_id'])

        return rental_completed
    

    def get_all_rentals(self, filters: dict):
        clean_filters = {
            column_name: column_value
            for column_name, column_value in filters.items() 
            if column_name in ALLOWED_FILTERS
        }
        
        return self.rental_repository.get_all_rentals(clean_filters)