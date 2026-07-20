
from flask import Blueprint, jsonify, request, Response

from models.user import User, UserRoles

from exceptions.user_exceptions import UsernameAlreadyExists, WrongUserCredentials, UserDoesNotExist
from exceptions.token_exceptions import InvalidToken




def create_user_blueprint(user_service):
    user_bp = Blueprint (
        'user_bp',
        __name__,
        url_prefix="/users"
    )

    #Routes

    #POST
    @user_bp.route('/register', methods=['POST'])
    def create_user():

        try:
            data = request.get_json()
            if(data.get('username') == None or data.get('password') == None):
                return Response(status=400)
            else:
                # Always explicitly map ONLY the fields that I want, otherwise the client may register themselves as 
                # user_role: "admin" if I unpack the whole dict like (**data).
                new_user = User(username=data.get('username'),
                                password=data.get('password'),
                                user_role=UserRoles.admin
                                )
                
                token = user_service.create_user(new_user)

                return jsonify(token=token)
            
        except UsernameAlreadyExists as error:
            return {"error": str(error)}, 409

    @user_bp.route('/login', methods=['POST'])
    def login_user():

        try:

            data = request.get_json()
            if(data.get('username') == None or data.get('password') == None):
                return Response(status=400)
            else:
                token = user_service.login_user(data.get('username'), 
                                                data.get('password'))

                return jsonify(token=token)

        except WrongUserCredentials as error:
            return {"error": str(error)}, 401    
        
    #GET
    @user_bp.route('/me', methods=['GET'])
    def get_me():
        
        try:
            #To fetch the Authorization header safely
            auth_header = request.headers.get('Authorization') #Returns None if missing

            if auth_header is None:
                return jsonify({"error": "Authorization header is missing"}), 401
        
            #Split 'Bearer' and the actual token
            #Expecting format: "Bearer <token_string>"
            header_parts = auth_header.split()

            if header_parts[0].lower() != 'bearer':
                return jsonify({"error": "Authorization header must start with 'Bearer'"}), 401
            elif len(header_parts) == 1:
                return jsonify({"error": "Token missing from Bearer header"}), 401
            elif len(header_parts) > 2:
                return jsonify({"error": "Authorization header must be 'Bearer <token>'"}), 401

            token = header_parts[1]

            #To process the token and get the user
            user = user_service.get_me(token)
            
            return jsonify(id=user.id, username=user.username)

        except InvalidToken as error:
            return {"error": str(error)}, 401
        except UserDoesNotExist as error:
            return {"error": str(error)}, 404

    return user_bp

