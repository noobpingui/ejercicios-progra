from sqlalchemy.orm import Session
from sqlalchemy import select
from models.car import Car

class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    #Create Car:
    def create_car(self, car: Car ):
        self.db.add(car) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(car) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        return car
    
    #Get Car by Id:
    def get_car_by_id(self, car_id: int):
        
        car = self.db.get(Car, car_id)

        return car
    
    #Update Car:
    def update_car(self, car_id: int, brand=None, model=None, year=None, status=None):
        
        #Obtengo el car por id
        car = self.get_car_by_id(car_id)
        
        #Modifico la data si el campo que llega no es None
        if brand is not None:
            car.brand = brand
        if model is not None:
            car.model = model
        if year is not None:
            car.year = year
        if status is not None:
            car.status = status

        #Guardo los cambios realizados
        self.db.commit()

        #Sincronizo la data
        self.db.refresh(car)

        return car
    
    #Delete Car:
    def delete_car(self, car_id: int):

        #Obtengo el car por id
        car = self.get_car_by_id(car_id)

        #Borro el car
        self.db.delete(car)

        #Guardo los cambios realizados
        self.db.commit()

        return None
    
    #Get all cars:
    def get_all_cars(self):
        
        #select(Car) -- contruye la query SELECT * FROM cars
        #self.db.execute(...) -- ejecuta la query y devuelve un resultado crudo en filas
        #.scalars() -- convierte las filas en objetos Python(Car), en lugar de tuplas
        # .all() -- materializa todo en una lista 
        #El flujo es: query → ejecutar → convertir a objetos → lista
        
        cars = self.db.execute(select(Car)).scalars().all()

        return cars
    
    #Metodo para asociar un car a un user
    def to_relate_car_to_user(self, car_id: int, user_id: int):
        
        #Obtengo el car por id
        car = self.get_car_by_id(car_id)

        #Modifico el user_id que llega como parametro
        car.user_id = user_id

        #Guardo los cambios realizados
        self.db.commit()

        #Sincronizo la data
        self.db.refresh(car)

        return car

