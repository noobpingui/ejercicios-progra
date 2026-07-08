
from models.user import User
from repositories.user_repository import UserRepository
from jwt_manager import JWT_Manager

class UserService():
    def __init__(self, user_repository: UserRepository, jwt_manager: JWT_Manager):
        self.user_repository = user_repository
        self.jwt_manager = jwt_manager

    #Insert/Register user
    def create_user(self, user: User):

        created_user = self.user_repository.create_user(user)

        user_data = {
            "id": int(created_user.id),
            "user_role": str(created_user.user_role)
        }

        token = self.jwt_manager.generate_token(user_data)

        return token
    
    #Login user
    def login_user(self, username: str, password: str):
        
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None
        if password != user.password:
            return None
        
        user_data = {
            "id": int(user.id),
            "user_role": str(user.user_role)
        }

        token = self.jwt_manager.generate_token(user_data)

        return token

    #get_me
    def get_me(self, token):

        decoded_token = self.jwt_manager.decode_token(token)

        if not decoded_token:
            return None
        
        user = self.user_repository.get_user_by_id(decoded_token["id"])

        return user      
    
        