# Routes - Responsable de:
# - HTTP
# - Request
# - Response
# - Convertir el Response / UserResponse, CarResponse, etc

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from models.car import CarCreate, CarResponse, CarStatusUpdate
from exceptions.car_exceptions import CarNotFound

#Blueprint registration

#Se crea el blueprint directamente en el modulo. Se cambia por el de abajo,
# car_bp = Blueprint 
#     'car_bp', 
#     __name__,
#     url_prefix="/cars"
# )

#Blueprint registration while applying Blueprint factory pattern
#Para poder inyectar la dependencia de car_service a routes. 
#Se puede hacer inyectando la clase, pero en routes se usa blueprint factory pattern,
#creando el blueprint dentro de una funcion para recibir el objeto como parametro.

def create_car_blueprint(car_service):
    car_bp = Blueprint (
        'car_bp', 
        __name__, 
        url_prefix="/cars")

    #Routes
    #GET
    @car_bp.route('/', methods=['GET'])
    def get_all_cars():
        # request.args.to_dict() convierte los query parameters del URL (?status=available&brand=Toyota) en un dict normal de Python
        # {"status": "available", "brand": "Toyota"}
        filters = request.args.to_dict()
        cars = car_service.get_all_cars(filters)

        return (jsonify(cars), 200)


    #POST
    @car_bp.route('/', methods=['POST'])
    def post_cars():

        try:
            body = request.get_json()

            #Se valida lo que llega con el model de CarCreate
            new_car = CarCreate(**body)

            created_car = car_service.create_car(new_car)

            #Se da forma al output en el response con el model de CarResponse
            created_car_response = CarResponse(**created_car).model_dump(mode='json')#Devuelve un dict con valores serializables

            return (jsonify(created_car_response),201)
        
        except ValidationError as error:
            return {"error": str(error)}, 400
        
    #PUT
    @car_bp.route('/<int:id>/status', methods=['PUT'])
    def put_car(id): #Flask inyecta el id recibido en el url, aqui

        try:
            body = request.get_json()

            #Se valida lo que llega con el model de CarStatusUpdate
            new_status = CarStatusUpdate(**body)

            car_service.update_car_status(id, new_status.status)

            #En este caso no es necesario devolver un response. Simplemente un mensaje de exito

            return jsonify({"message": "Car status updated successfully"}), 200
        
        except ValidationError as error:
            return {"error": str(error)}, 400
        
        except CarNotFound as error:
            return {"error": str(error)}, 404



    return car_bp