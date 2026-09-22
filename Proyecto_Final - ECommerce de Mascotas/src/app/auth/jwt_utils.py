import datetime

import jwt

from app.config import Config


def _read_key(path):
    with open(path, "rb") as key_file:
        return key_file.read()


def encode_token(user_id, role):
    private_key = _read_key(Config.JWT_PRIVATE_KEY_PATH)
    now = datetime.datetime.now(datetime.timezone.utc)

    claims = {
        "user_id": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=Config.JWT_EXP_MINUTES),
    }

    return jwt.encode(claims, private_key, algorithm=Config.JWT_ALGORITHM)


def decode_token(token):
    public_key = _read_key(Config.JWT_PUBLIC_KEY_PATH)
    return jwt.decode(token, public_key, algorithms=[Config.JWT_ALGORITHM])
