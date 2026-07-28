from flask import Blueprint, jsonify, request, Response, g

from models.user import User, UserRoles

from exceptions.user_exceptions import UsernameAlreadyExists, WrongUserCredentials, UserDoesNotExist
from decorators import require_auth

def create_user_blueprint(user_service, jwt_manager):
    user_bp = Blueprint(
        'user_bp',
        __name__,
        url_prefix="/users"
    )

    #POST
    @user_bp.route('/register', methods=['POST'])
    def create_user():
        try:
            data = request.get_json()
            if data.get('username') is None or data.get('password') is None:
                return Response(status=400)

            # Always explicitly map ONLY the fields that I want, otherwise the client may register themselves as
            # user_role: "admin" if I unpack the whole dict like (**data).
            new_user = User(username=data.get('username'),
                            password=data.get('password'),
                            user_role=UserRoles.user
                            )

            token = user_service.create_user(new_user)

            return jsonify(token=token), 201

        except UsernameAlreadyExists as error:
            return {"error": str(error)}, 409


    @user_bp.route('/login', methods=['POST'])
    def login_user():
        try:
            
            data = request.get_json()
            if data.get('username') is None or data.get('password') is None:
                return Response(status=400)

            token = user_service.login_user(data.get('username'),
                                            data.get('password'))

            return jsonify(token=token), 200

        except WrongUserCredentials as error:
            return {"error": str(error)}, 401


    #GET
    @user_bp.route('/me', methods=['GET'])
    @require_auth(jwt_manager)
    def get_me():
        try:

            user_id = g.decoded_token["id"]

            user = user_service.get_me(user_id)

            
            return jsonify(
                id=user.id,
                username=user.username
            ), 200

        except UserDoesNotExist as error:
            return {"error": str(error)}, 404


    return user_bp
