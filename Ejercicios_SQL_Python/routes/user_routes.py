
# Routes - Responsable de:
# - HTTP
# - Request
# - Response
# - Convertir el Response / UserResponse, CarResponse, etc


from flask import Blueprint, jsonify, request

from pydantic import ValidationError
from exceptions.user_exceptions import UserUnderAge, UserEmailAlreadyExists, UsernameAlreadyExists, UserNotFound, UserIsDelinquent

from models.user import UserCreate, UserResponse, UserStatusUpdate

#Blueprint registration

#Se crea el blueprint directamente en el modulo. Se cambia por el de abajo,
# user_bp = Blueprint 
#     'user_bp', 
#     __name__,
#     url_prefix="/users"
# )

#Blueprint registration while applying Blueprint factory pattern
#Para poder inyectar la dependencia de user_service a routes. 
#Se puede hacer inyectando la clase, pero en routes se usa blueprint factory pattern,
#creando el blueprint dentro de una funcion para recibir el objeto como parametro.
def create_user_blueprint(user_service):
    user_bp = Blueprint (
        'user_bp', 
        __name__, 
        url_prefix="/users")


    #Routes
    #GET
    @user_bp.route('/', methods=['GET'])
    def get_all_users():
        # request.args.to_dict() convierte los query parameters del URL (?status=active&name=Juan) en un dict normal de Python
        # {"status": "active", "name": "Juan"}
        filters = request.args.to_dict()
        users = user_service.get_all_users(filters)

        return (jsonify(users), 200)

    #POST
    @user_bp.route('/', methods=['POST'])
    def post_users():

        try:
            body = request.get_json()

            #Se valida lo que llega con el model de UserCreate
            new_user = UserCreate(**body)

            created_user = user_service.create_user(new_user)

            #Se da forma al output en el response con el model de UserResponse
            created_user_response = UserResponse(**created_user).model_dump(mode='json')#Devuelve un dict con valores serializables

            return (jsonify(created_user_response),201)
        
        except ValidationError as error:
            return {"error": str(error)}, 400
        
        except UserUnderAge as error:
            return {"error": str(error)}, 409
        
        except UserEmailAlreadyExists as error:
            return {"error": str(error)}, 409
        
        except UsernameAlreadyExists as error:
            return {"error": str(error)}, 409

    #PUT - Status
    @user_bp.route('/<int:id>/status', methods=['PUT'])
    def put_user_status(id): #Flask inyecta el id recibido en el url, aqui

        try:
            body = request.get_json()

            #Se valida lo que llega con el model de UserStatusUpdate
            new_status = UserStatusUpdate(**body)

            user_service.update_user_status(id, new_status.status)

            #En este caso no es necesario devolver un response. Simplemente un mensaje de exito

            return jsonify({"message": "User status updated successfully"}), 200
        
        except ValidationError as error:
            return {"error": str(error)}, 400
        
        except UserNotFound as error:
            return {"error": str(error)}, 404


    #PUT - Is_delinquent
    @user_bp.route('/<int:id>/is_delinquent', methods=['PUT'])
    def put_user_is_delinquent(id): #Flask inyecta el id recibido en el url, aqui

        try:
            user_service.flag_user_as_delinquent(id)

            #En este caso no es necesario devolver un response. Simplemente un mensaje de exito
            return jsonify({"message": "User has been flagged as delinquent"}), 200
        
        except UserNotFound as error:
            return {"error": str(error)}, 404
        
        except UserIsDelinquent as error:
            return {"error": str(error)}, 409

    return user_bp

    