
from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select


class UserRepository:
    def __init__(self, db: Session):
        self.db = db


    #INSERT/REGISTER USER
    def create_user(self, user: User ):
        self.db.add(user) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(user) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        return user
    
    def get_user_by_id(self, user_id):
        
        user = self.db.get(User, user_id)

        return user


    def get_user_by_username(self, username: str):
        
        stmt = select(User).where(User.username == username)

        user = self.db.execute(stmt).scalars().first()

        return user