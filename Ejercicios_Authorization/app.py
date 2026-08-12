
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException #Libreria base para manejar todos los error HTTP de Flask (400,404, etc) 

import logging

logging.basicConfig(level=logging.INFO) #Para que se vean mejor los logger.warning()



#DB
#from db import Session
from db import Session

#JWT_Manager
from jwt_manager import JWT_Manager

#Redis
from cache import redis_client

#User
from repositories.user_repository import UserRepository
from services.user_service import UserService
from routes.user_route import create_user_blueprint

#Product
from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from routes.product_route import create_product_blueprint

#Invoice
from repositories.invoice_repository import InvoiceRepository
from services.invoice_service import InvoiceService
from routes.invoice_route import create_invoice_blueprint



#Instancing Flask app
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = False

#JWT_Manager
jwt_manager = JWT_Manager('.\private_key.pem', '.\public_key.pem')

#Repositories -> dependencies
user_repository = UserRepository(Session)
product_repository = ProductRepository(Session, redis_client)
invoice_repository = InvoiceRepository(Session)

#Services -> dependencies
user_service = UserService(user_repository, jwt_manager)
product_service = ProductService(product_repository)
invoice_service = InvoiceService(invoice_repository, product_repository)

#Route/Blueprint registration
app.register_blueprint(create_user_blueprint(user_service, jwt_manager))
app.register_blueprint(create_product_blueprint(product_service, jwt_manager))
app.register_blueprint(create_invoice_blueprint(invoice_service, jwt_manager))



#Flask calls this automatically at the end of every single request, no matter which route handled it
@app.teardown_appcontext 
def shutdown_session(exception=None): #To properly shutdown a session
    Session.remove()


@app.errorhandler(Exception) # Paraatrapar cualquier exception no manejada en cualquier ruta
def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        return jsonify(error=error.description), error.code
    app.logger.exception("Unhandled exception") #Permite loggear el traceback completo en el server

    return jsonify(error="Internal server error"), 500 # Para los error code 500

#App initializer
if __name__ == "__main__":
    app.run(debug=True)
