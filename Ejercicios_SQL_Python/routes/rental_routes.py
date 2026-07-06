
# Routes - Responsable de:
# - HTTP
# - Request
# - Response
# - Convertir el Response / UserResponse, CarResponse, etc

from flask import Blueprint, jsonify, request

from pydantic import ValidationError
from exceptions.rental_exceptions import UserNotExists, UserNotActive, UserIsDelinquent, CarNotExists, CarNotAvailable, RentalNotFound, RentalCompletedAlready

from models.rental import RentalCreate, RentalResponse

#Blueprint registration

#Se crea el blueprint directamente en el modulo. Se cambia por el de abajo,
# rental_bp = Blueprint 
#     'rental_bp', 
#     __name__,
#     url_prefix="/users"
# )

#Blueprint registration while applying Blueprint factory pattern
#Para poder inyectar la dependencia de rental_service a routes. 
#Se puede hacer inyectando la clase, pero en routes se usa blueprint factory pattern,
#creando el blueprint dentro de una funcion para recibir el objeto como parametro.
def create_rental_blueprint(rental_service):
    rental_bp = Blueprint (
        'rental_bp',
        __name__,
        url_prefix="/rentals"
    )

    #Routes

    #GET
    @rental_bp.route('/', methods=['GET'])
    def get_all_rentals():
        # request.args.to_dict() convierte los query parameters del URL (?status=active&car_id=21) en un dict normal de Python
        # {"status": "active", "car_id": "21"}
        filters = request.args.to_dict()
        rentals = rental_service.get_all_rentals(filters)

        return (jsonify(rentals), 200)



    #POST
    @rental_bp.route('/', methods=['POST'])
    def post_rentals():

        try:
            body = request.get_json()

            #Se valida lo que llega con el model de RentalCreate
            new_rental = RentalCreate(**body)

            created_rental = rental_service.create_rental(new_rental)

            #Se da forma al output en el response con el model de UserResponse
            created_rental_response = RentalResponse(**created_rental).model_dump(mode='json')#Devuelve un dict con valores serializables

            return (jsonify(created_rental_response),201)
        
        except ValidationError as error:
            return {"error": str(error)}, 400
        
        except UserNotExists as error:
            return {"error": str(error)}, 404
        
        except UserNotActive as error:
            return {"error": str(error)}, 409
        
        except UserIsDelinquent as error:
            return {"error": str(error)}, 409
        
        except CarNotExists as error:
            return {"error": str(error)}, 404
        
        except CarNotAvailable as error:
            return {"error": str(error)}, 409

    #PUT
    @rental_bp.route('/<int:id>/status', methods=['PUT'])
    def put_rental(id): #Flask inyecta el id recibido en el url, aqui

        try:
            
            rental_service.complete_rental(id)

            #En este caso no es necesario devolver un response. Simplemente un mensaje de exito

            return jsonify({"message": "Rental status updated successfully"}), 200
        
        except ValidationError as error:
            return {"error": str(error)}, 400
        
        except RentalNotFound as error:
            return {"error": str(error)}, 404
        
        except RentalCompletedAlready as error:
            return {"error": str(error)}, 409

    return rental_bp