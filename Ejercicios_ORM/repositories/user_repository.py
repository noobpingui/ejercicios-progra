from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from exceptions.user_exceptions import UserNotFound

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    #Create User:
    def create_user(self, user: User ):
        self.db.add(user) #Para registrar el objeto en la sesion
        self.db.commit() #Para confirmar la transaccion en la DB
        self.db.refresh(user) #Para sincronizar el objeto con los datos que devuelve la DB, por el ejemplo el ID que se genera

        return user
    
    #Get User by Id:
    def get_user_by_id(self, user_id: int):
        
        user = self.db.get(User, user_id)

        if user is None:
            raise UserNotFound(f"The user with id:{user_id} was not found")

        return user
    
    #Update User:
    def update_user(self, user_id: int, name=None, email=None, status=None):
        
        #Obtengo el user por id
        user = self.get_user_by_id(user_id)
        
        #Modifico la data si el campo que llega no es None
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if status is not None:
            user.status = status

        #Guardo los cambios realizados
        self.db.commit()

        #Sincronizo la data
        self.db.refresh(user)

        return user
    
    #Delete User:
    def delete_user(self, user_id: int):

        #Obtengo el user por id
        user = self.get_user_by_id(user_id)

        #Borro el user
        self.db.delete(user)

        #Guardo los cambios realizados
        self.db.commit()

        return user
    
    #Get all users:
    def get_all_users(self):
        
        #select(User) -- contruye la query SELECT * FROM users
        #self.db.execute(...) -- ejecuta la query y devuelve un resultado crudo en filas
        #.scalars() -- convierte las filas en objetos Python(User), en lugar de tuplas
        # .all() -- materializa todo en una lista 
        #El flujo es: query → ejecutar → convertir a objetos → lista
        
        users = self.db.execute(select(User)).scalars().all()

        return users