
# El Service tiene métodos “de negocio”, el Repository tiene métodos “de datos”

# Repository - Responsable de:
# - Ejecutar SQL
# - Hablar con PgManager
# - Devolver datos

from db_connection import PgManager 
from models.rental import RentalCreate,RentalStatus

class RentalRepository:
    def __init__(self, db: PgManager):
        self.db = db


    # WHERE 1=1 es siempre verdadero — es un placeholder que permite encadenar AND condiciones sin saber cual llegara
    # primero. Si no hay filtros, la condicion no afecta el resultado
    def get_all_rentals(self, filters: dict):
        query = """
        SELECT  
            *
        FROM lyfter_car_rental.rental
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
        # execute_query espera los valores como argumentos separados, no como lista. El * desempaca ["active", 21] en
        # "active", 21
        result = self.db.execute_query(query, *params)

        if not result:
            return []
        
        return result
        #Devuelve la lista completa de filas (no solo la primera como en get_rental_by_id).

    def get_rental_by_id(self, id: int) -> dict | None:
        query = """
        SELECT  
            id,
            user_id,
            car_id,
            rental_date,
            status
        FROM lyfter_car_rental.rental
        WHERE id = %s
        """

        result = self.db.execute_query(query, id)

        if not result:
            return None
        
        return dict(result[0])

    
    def create_rental(self, rental: RentalCreate) -> dict | None:
        query = """
        INSERT INTO lyfter_car_rental.rental(user_id, car_id)
        VALUES 
        (
            %s,
            %s
        )
        RETURNING
            id,
            user_id,
            car_id,
            rental_date,
            status
        """

        result = self.db.execute_query(query, rental.user_id, rental.car_id)

        if not result:
            return None
        
        return dict(result[0])

    def complete_rental(self, id: int) -> None:
        query = """
        UPDATE lyfter_car_rental.rental
            SET status = 'completed'
        WHERE id = %s
        """

        self.db.execute_query(query, id)

        return None
    