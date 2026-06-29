from db_connection import PgManager
from flask import Flask

from repositories.user_repository import UserRepository
from repositories.car_repository import CarRepository
from repositories.rental_repository import RentalRepository

from services.user_service import UserService
from services.car_service import CarService
from services.rental_service import RentalService

from routes.user_routes import create_user_blueprint
from routes.car_routes import create_car_blueprint
from routes.rental_routes import create_rental_blueprint

import os
from dotenv import load_dotenv

#Instancing app
app = Flask(__name__)

#To load variables included in .env file
load_dotenv()

#To read the information usnig os.getenv
db_name = os.getenv('DB_NAME') 
db_user = os.getenv('DB_USER') 
db_password = os.getenv('DB_PASSWORD') 
db_host = os.getenv('DB_HOST') 
db_port = os.getenv('DB_PORT')

#DATABASE
db_manager = PgManager(
    db_name = db_name, 
    user = db_user,
    password = db_password,
    host = db_host,
    port = db_port
)

#Dependencies

#Repository
user_repository = UserRepository(db_manager)
car_repository = CarRepository(db_manager)
rental_repository = RentalRepository(db_manager)

#Service
user_service = UserService(user_repository)
car_service = CarService(car_repository)
rental_service = RentalService(rental_repository, user_repository, car_repository)

#Route/Blueprint registration
app.register_blueprint(create_user_blueprint(user_service))
app.register_blueprint(create_car_blueprint(car_service))
app.register_blueprint(create_rental_blueprint(rental_service))

#App initializer
if __name__ == "__main__":
    app.run(debug=True)