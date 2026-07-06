
# El Service tiene métodos “de negocio”, el Repository tiene métodos “de datos”

# Service - Responsable de:

# - Validar edad mínima
# - Validar email duplicado
# - Validar username duplicado
# - Crear usuario
# - Aplicar reglas de negocio


from dateutil.relativedelta import relativedelta #For calculate age with birthday
from datetime import date
from exceptions.user_exceptions import UserUnderAge, UserEmailAlreadyExists, UsernameAlreadyExists, UserNotFound, UserIsDelinquent
from models.user import UserCreate, UserStatus
from repositories.user_repository import UserRepository

# Para los filters:
# ALLOWED_FILTERS define que columnas se permiten como filtro. El dict comprehension recorre los filtros que llegaron
# del request y solo conserva los que estan en esa lista — descartando cualquier key invalida o maliciosa. El dict
# limpio se pasa al repository que construye el SQL dinamicamente.
ALLOWED_FILTERS = {"id", "name", "email", "username", "status", "is_delinquent"}

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    def _calculate_age(self, birth_date: date) -> int:
        age = relativedelta(date.today(), birth_date).years
        
        return age
    
    def _user_not_found(self, user_id: int):
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            raise UserNotFound(f"The user with the ID:{user_id} does not exist")
        
        return existing_user
    
    def _user_is_delinquent(self, user: dict):
        if user['is_delinquent'] != False:
            raise UserIsDelinquent("The user has been flagged as delinquent already")

        
    #Metodos para User
    def create_user(self, user: UserCreate):
        
        #Age validation
        age = self._calculate_age(user.birth_date)
        if age < 18:
            raise UserUnderAge("The user is under 18 years old")

        #Duplicated email vallidation
        existing_email = self.user_repository.get_user_by_email(user.email)
        if existing_email:
            raise UserEmailAlreadyExists("Email already exists")
        
        #Duplicated username vallidation
        existing_username = self.user_repository.get_user_by_username(user.username)
        if existing_username:
            raise UsernameAlreadyExists("Username already exists")
        
        #User creation
        created_user = self.user_repository.create_user(user)

        return created_user
    

    def get_all_users(self, filters: dict):
        clean_filters = {
            column_name: column_value
            for column_name, column_value in filters.items() 
            if column_name in ALLOWED_FILTERS
        }
        
        return self.user_repository.get_all_users(clean_filters)


    def update_user_status(self, user_id: int, status: UserStatus):
        self._user_not_found(user_id)
        user_status = self.user_repository.update_user_status(status, user_id)

        return user_status
    
    def flag_user_as_delinquent(self, user_id: int):
        user = self._user_not_found(user_id)
        self._user_is_delinquent(user)

        flagged_user = self.user_repository.flag_user_as_delinquent(user_id)

        return flagged_user