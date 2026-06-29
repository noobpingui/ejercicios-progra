
# El Service tiene métodos “de negocio”, el Repository tiene métodos “de datos”

# Service - Responsable de:

# - Crear car
# - Aplicar reglas de negocio

from repositories.car_repository import CarRepository
from models.car import CarCreate, CarStatus
from exceptions.car_exceptions import CarNotFound

# Para los filters:
# ALLOWED_FILTERS define que columnas se permiten como filtro. El dict comprehension recorre los filtros que llegaron
# del request y solo conserva los que estan en esa lista — descartando cualquier key invalida o maliciosa. El dict
# limpio se pasa al repository que construye el SQL dinamicamente.
ALLOWED_FILTERS = {"id", "brand", "model", "year", "status"}

class CarService:
    def __init__(self, car_repository: CarRepository):
        self.car_repository = car_repository
    
    #No es necesaria porque ya lo valido en el BaseModel
    # def car_years_allowed(self, year) -> int:
    #     if year < 2011 or year > 2026:
    #         raise CarYearNotAllowed("The year must be between 2011 and 2026")

    #     return year

    def _car_not_found(self, car_id: int):
        existing_car = self.car_repository.get_car_by_id(car_id)
        if not existing_car:
            raise CarNotFound(f"The car with the ID:{car_id} does not exist")

    def create_car(self, car: CarCreate):
        
        #Al final no es necesaria porque se valida en el Basemodel
        #Year validation
        #self.car_years_allowed(car.year) 

        #car creation
        created_car = self.car_repository.create_car(car)

        return created_car
    

    def get_all_cars(self, filters: dict):
        clean_filters = {
            column_name: column_value
            for column_name, column_value in filters.items() 
            if column_name in ALLOWED_FILTERS
        }
        
        return self.car_repository.get_all_cars(clean_filters)
    
    def update_car_status(self, car_id: int, status: CarStatus):
        self._car_not_found(car_id)
        car_status = self.car_repository.update_car_status(status ,car_id)

        return car_status