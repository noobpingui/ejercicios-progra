
from flask import Flask

#DB
from db import SessionLocal

#JWT_Manager
from jwt_manager import JWT_Manager

#User
from repositories.user_repository import UserRepository
from services.user_service import UserService
from routes.user_route import create_user_blueprint

#Product
from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from routes.product_route import create_product_blueprint



#Instancing Flask app
app = Flask(__name__)

#To create a session
session = SessionLocal()

#JWT_Manager
jwt_manager = JWT_Manager('.\private_key.pem', '.\public_key.pem')

#Repositories -> dependencies
user_repository = UserRepository(session)
product_repository = ProductRepository(session)

#Services -> dependencies
user_service = UserService(user_repository, jwt_manager)
product_service = ProductService(product_repository)

#Route/Blueprint registration
app.register_blueprint(create_user_blueprint(user_service))
app.register_blueprint(create_product_blueprint(product_service, jwt_manager))


#App initializer
if __name__ == "__main__":
    app.run(debug=True)
