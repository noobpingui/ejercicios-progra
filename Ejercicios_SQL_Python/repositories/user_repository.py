
# El Service tiene métodos “de negocio”, el Repository tiene métodos “de datos”

# Repository - Responsable de:
# - Ejecutar SQL
# - Hablar con PgManager
# - Devolver datos

from db_connection import PgManager 
from models.user import UserCreate, UserStatus

class UserRepository:
    def __init__(self, db: PgManager):
        self.db = db


    def create_user(self, user: UserCreate) -> dict | None:
        query = """
        INSERT INTO lyfter_car_rental.user_account(name, email, username, password_hash, birth_date)
        VALUES 
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        RETURNING
            id,
            name,
            email,
            username,
            birth_date,
            status,
            is_delinquent;
        """

        result = self.db.execute_query(query, user.name, user.email, user.username, user.password_hash, user. birth_date)

        if not result:
            return None
        
        return dict(result[0])
    
    # WHERE 1=1 es siempre verdadero — es un placeholder que permite encadenar AND condiciones sin saber cual llegara
    # primero. Si no hay filtros, la condicion no afecta el resultado
    def get_all_users(self, filters: dict):
        query = """
        SELECT  
            id,
            name,
            email,
            username,
            birth_date,
            status,
            is_delinquent
        FROM lyfter_car_rental.user_account
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
        # execute_query espera los valores como argumentos separados, no como lista. El * desempaca ["active", "Juan"] en
        # "active", "Juan"
        result = self.db.execute_query(query, *params)

        if not result:
            return []
        
        return result
        #Devuelve la lista completa de filas (no solo la primera como en get_user_by_id).

    def get_user_by_email(self, email: str) -> dict | None:
        query = """
        SELECT  
            id,
            name,
            email,
            username,
            birth_date,
            status,
            is_delinquent
        FROM lyfter_car_rental.user_account
        WHERE email = %s
        """

        result = self.db.execute_query(query, email)

        if not result:
            return None
        
        return dict(result[0])
    
    def get_user_by_username(self, username: str) -> dict | None:
        query = """
        SELECT  
            id,
            name,
            email,
            username,
            birth_date,
            status,
            is_delinquent
        FROM lyfter_car_rental.user_account
        WHERE username = %s
        """

        result = self.db.execute_query(query, username)

        if not result:
            return None
        
        return dict(result[0])
    
    def get_user_by_id(self, id: int) -> dict | None:
        query = """
        SELECT  
            id,
            name,
            email,
            username,
            birth_date,
            status,
            is_delinquent
        FROM lyfter_car_rental.user_account
        WHERE id = %s
        """

        result = self.db.execute_query(query, id)

        if not result:
            return None
        
        return dict(result[0])
    
    def update_user_status(self, status: UserStatus, id: int) -> None:
        query = """
        UPDATE lyfter_car_rental.user_account
            SET status = %s
        WHERE id = %s
        """

        self.db.execute_query(query, status, id)

        return None
    
    def flag_user_as_delinquent(self, id: int) -> None:
        query = """
        UPDATE lyfter_car_rental.user_account
            SET is_delinquent = true
        WHERE id = %s
        """

        self.db.execute_query(query, id)

        return None