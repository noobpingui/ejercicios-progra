import jwt
import datetime
from typing import Dict, Any


class JWT_Manager:
    def __init__(self, private_key_path: str, public_key_path: str):
        #To load the RSA keys from disk
        with open(private_key_path,"r") as file:
            self.private_key = file.read()

        with open(public_key_path,"r") as file:
            self.public_key = file.read()
        
        self.algorithm = "RS256"

    def generate_token(self, data: Dict[str, Any], expires_in_minutes: int = 30) -> str:
        try:

            #To creaet a new dict, add the expiration data below and keep the original dict untouched/clean
            payload = data.copy()

            #Standard security
            now = datetime.datetime.now(datetime.timezone.utc)
            payload.update({
                "iat": now,  #issued at
                "exp": now + datetime.timedelta(minutes=expires_in_minutes) #Expiration
            })

            #To encode with private key
            encoded = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
            return encoded
        
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {e}")
            return None

    def decode_token(self, token:str):

        #To verify and decode a JWT Token using the public key
        try:
            decoded = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            return decoded
        
        except jwt.ExpiredSignatureError:
            print("The token has expired")
            return None
        
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {e}")
            return None