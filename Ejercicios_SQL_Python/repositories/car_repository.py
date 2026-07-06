
# El Service tiene métodos “de negocio”, el Repository tiene métodos “de datos”

# Repository - Responsable de:
# - Ejecutar SQL
# - Hablar con PgManager
# - Devolver datos

from db_connection import PgManager 
from models.car import CarCreate, CarStatus

class CarRepository:
    def __init__(self, db: PgManager):
        self.db = db

    def create_car(self, car: CarCreate) -> dict | None:
        query = """
        INSERT INTO lyfter_car_rental.car(brand, model, year)
        VALUES 
        (
            %s,
            %s,
            %s
        )
        RETURNING
            id,
            brand,
            model,
            year,
            status;
        """

        result = self.db.execute_query(query, car.brand, car.model, car.year)

        if not result:
            return None
        
        return dict(result[0])
    
    # WHERE 1=1 es siempre verdadero — es un placeholder que permite encadenar AND condiciones sin saber cual llegara
    # primero. Si no hay filtros, la condicion no afecta el resultado
    def get_all_cars(self, filters: dict):
        query = """
        SELECT  
            *
        FROM lyfter_car_rental.car
        WHERE 1=1 
        """

        # Por cada filtro que llego (ya limpio desde el service), agrega una condicion AND al SQL y el valor correspondiente a
        # la lista params. Al final del loop, query y params estan sincronizados — cada %s en el query tiene su valor en la
        # misma posicion en params
        params =[]

        for column, value in filters.items():
            query += f" AND {column} = %s" 
            params.append(value)

        query += " ORDER BY id ASC"

        # *params al ejecutar
        # self.db.execute_query(query, *params)
        # execute_query espera los valores como argumentos separados, no como lista. El * desempaca ["available", "Toyota"] en
        # "available", "Toyota"
        result = self.db.execute_query(query, *params)

        if not result:
            return []
        
        return result
        #Devuelve la lista completa de filas (no solo la primera como en get_car_by_id).

    def get_car_by_id(self, id: int) -> dict | None:
        query = """
        SELECT  
            id,
            brand,
            model,
            year,
            status
        FROM lyfter_car_rental.car
        WHERE id = %s
        """

        result = self.db.execute_query(query, id)

        if not result:
            return None
        
        return dict(result[0])
    
    def update_car_status(self, status: CarStatus, id: int) -> None:
        query = """
        UPDATE lyfter_car_rental.car
            SET status = %s
        WHERE id = %s
        """

        self.db.execute_query(query, status, id)

        return None