

from flask import Blueprint, jsonify, request, Response
from models.product import Product

from jwt_manager import JWT_Manager

from exceptions.product_exceptions import DuplicatedProductName, ProductNotExist
from exceptions.token_exceptions import InvalidToken

def create_product_blueprint(product_service, jwt_manager):
    product_bp = Blueprint (
        'product_bp',
        __name__,
        url_prefix="/products"
    )

    #Routes

    #Post
    @product_bp.route('/', methods=['POST'])
    def create_product():

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

            decoded_token = jwt_manager.decode_token(token)

            if decoded_token is None:
                raise InvalidToken("Invalid token")

            if decoded_token["user_role"] != "admin":
                
                return jsonify({"error": "Forbidden: admin access required"}), 403
            
            else:

                data = request.get_json()
                if(data.get('name') == None or data.get('price') == None or data.get('quantity') == None):
                    return Response(status=400)
                else:
                    new_product = Product(name=data.get('name'),
                                          price=data.get('price'),
                                          quantity=data.get('quantity'))

                    product = product_service.create_product(new_product)

                    return jsonify(id=product.id, name=product.name, price=product.price, quantity=product.quantity)
        
        except DuplicatedProductName as error:
            return {"error": str (error)}, 400
        except InvalidToken as error:
            return {"error": str (error)}, 401
        


    #GET    
    @product_bp.route('/<int:id>', methods=['GET'])
    def get_product_by_id(id):
        
        try:

            #To fetch the Autorization header safely
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

            decoded_token = jwt_manager.decode_token(token)

            if decoded_token is None:
                raise InvalidToken("Invalid token")
            
            else:
            
                product = product_service.get_product_by_id(id)
                
                return jsonify(id=product.id, name=product.name, price=product.price, quantity=product.quantity)
                
        except ProductNotExist as error:
            return {"error": str (error)}, 404
        except InvalidToken as error:
            return {"error": str (error)}, 401
        

    #DELETE
    @product_bp.route('/<int:id>', methods=['DELETE'])
    def delete_product(id):

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

            decoded_token = jwt_manager.decode_token(token)

            if decoded_token is None:
                raise InvalidToken("Invalid token")

            if decoded_token["user_role"] != "admin":
                return jsonify({"error": "Forbidden: admin access required"}), 403
            
            else:
            
                product = product_service.get_product_by_id(id)
                
                product_service.delete_product(product.id)

                return jsonify(f"The product with the ID:{product.id} has been successfully deleted"), 200

        except ProductNotExist as error:
            return {"error": str (error)}, 404
        except InvalidToken as error:
            return {"error": str (error)}, 401
        
    
    #PUT
    @product_bp.route('/<int:id>', methods=['PUT'])
    def update_product(id):

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

            decoded_token = jwt_manager.decode_token(token)

            if decoded_token is None:
                raise InvalidToken("Invalid token")

            if decoded_token["user_role"] != "admin":
                return jsonify({"error": "Forbidden: admin access required"}), 403
            
            else:
            
                data = request.get_json()
        
                updated_product = product_service.update_product(id, data.get('name'), data.get('price'), data.get('quantity'))

                return jsonify(id=updated_product.id, name=updated_product.name, price=updated_product.price, quantity=updated_product.quantity), 200
                           
        except ProductNotExist as error:
            return {"error": str (error)}, 404
        except InvalidToken as error:
            return {"error": str (error)}, 401


    return product_bp