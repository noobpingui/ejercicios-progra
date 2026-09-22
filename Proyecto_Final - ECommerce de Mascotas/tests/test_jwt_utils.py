import uuid

import jwt as pyjwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.auth.jwt_utils import decode_token, encode_token
from app.config import Config


def test_encode_and_decode_roundtrip():
    user_id = str(uuid.uuid4())
    role = "admin"

    token = encode_token(user_id, role)
    decoded = decode_token(token)

    assert decoded["user_id"] == user_id
    assert decoded["role"] == role
    assert "iat" in decoded
    assert "exp" in decoded


def test_expired_token_raises(monkeypatch):
    monkeypatch.setattr(Config, "JWT_EXP_MINUTES", -1)

    token = encode_token(str(uuid.uuid4()), "regular_user")

    with pytest.raises(pyjwt.ExpiredSignatureError):
        decode_token(token)


def test_invalid_signature_raises():
    bogus_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    bogus_pem = bogus_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    token = pyjwt.encode(
        {"user_id": str(uuid.uuid4()), "role": "regular_user"},
        bogus_pem,
        algorithm=Config.JWT_ALGORITHM,
    )

    with pytest.raises(pyjwt.InvalidSignatureError):
        decode_token(token)
