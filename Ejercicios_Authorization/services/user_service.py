

from exceptions.user_exceptions import UsernameAlreadyExists, WrongUserCredentials, UserDoesNotExist
from exceptions.token_exceptions import InvalidToken

from models.user import User
from repositories.user_repository import UserRepository

from jwt_manager import JWT_Manager
import bcrypt

class UserService():
    def __init__(self, user_repository: UserRepository, jwt_manager: JWT_Manager):
        self.user_repository = user_repository
        self.jwt_manager = jwt_manager

    #Insert/Register user
    def create_user(self, user: User):

        #Duplicated username validation
        existing_username = self.user_repository.get_user_by_username(user.username)
        if existing_username:
            raise UsernameAlreadyExists("Username already exists")

        #Hashing the password before passing it to the repository to save it to the DB.
        hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        #bcrypt returns bytes, not a string. PostgreSQL with SQLAlchemy expects a string for the
        #password column, so it's neccesary to decode it back after hashing it.
        user.password = hashed.decode('utf-8')

        created_user = self.user_repository.create_user(user)

        user_data = {
            "id": int(created_user.id),
            "user_role": created_user.user_role.value
        }

        token = self.jwt_manager.generate_token(user_data, 30)

        return token
    
    #Login user
    def login_user(self, username: str, password: str):
        
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise WrongUserCredentials("Wrong credentials")
        
        #  checkpw returns True if the plain password matches the stored hash, False otherwise
        #  bcrypt.checkpw expects both arguments as bytes, so it's necesary to encode both
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise WrongUserCredentials("Wrong credentials")
        
        user_data = {
            "id": int(user.id),
            "user_role": user.user_role.value
        }

        token = self.jwt_manager.generate_token(user_data, 30)

        return token

    #get_me
    def get_me(self, user_id: int):

        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise UserDoesNotExist("The user does not exist")

        return user
    
        