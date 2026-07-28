from flask import request, jsonify, g 
from functools import wraps

# g = Objeto de contexto de Flask que permite compartir datos entre funciones durante la peticion HTTP actual

# closure = Un closure es una funcion que recuerda las variables de la funcion donde fue creada, 
# incluso despues de que esa funcion ya termino de ejecutarse 
# Condiciones para que exista un closure:
# 1. La funcion hija esta anidada dentro de otra funcion.
# 2. La funcion hija usa una variable de la funcion padre.
# 3. La funcion hija sigue existiendo despues de que la funcion padre termina 
# (normalmente porque se retorna o se guarda en algun lugar)


#Regular user-role
def require_auth(jwt_manager): #Su unico trabajo es recibir jwt_manager y devolver un decorador
    def decorator(func): #Recibimos la funcion que se va a decorar. Su trabajo es crear el wrapper y devolverlo
        @wraps(func)  #Conserva los metadatos de la función original en el wrapper
        def wrapper(*args, **kwargs): # Ejecuta la logica de autenticacion antes de llamar a la funcion original
                                      # Usamos *args, **kwargs porque no sabemos los argumentos que recibe cada metodo


            #Validacion de el token
            auth_header = request.headers.get('Authorization')

            if auth_header is None:
                return jsonify({"error": "Authorization header is missing"}), 401

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
                return jsonify({"error": "Invalid token"}), 401

            #Utilizamos g para almacenar el token y poder utilizarlo despues dentro de la funcion original.
            #g solamente vive en la misma peticion http y despues muere
            g.decoded_token = decoded_token

            #Llamamos a la funcion original y almacenamos el resultado
            result = func(*args, **kwargs)

            #Retornamos el resultado de la funcicion original
            return result
        return wrapper
    return decorator

#Admin user-role
def require_admin(jwt_manager):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get('Authorization')

            if auth_header is None:
                return jsonify({"error": "Authorization header is missing"}), 401

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
                return jsonify({"error": "Invalid token"}), 401

            if decoded_token["user_role"] != "admin":
                return jsonify({"error": "Forbidden: admin access required"}), 403

            #g.decoded_token = decoded_token
            #No necesaria ya que ninguna ruta la esta consumiendo

            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator
