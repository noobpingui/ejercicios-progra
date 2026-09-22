from sqlalchemy import text

from app.extensions import engine, redis_client


def test_create_app_returns_a_flask_app(app):
    assert app is not None
    assert app.name == "app"


def test_database_connection_is_established():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_redis_connection_is_established():
    assert redis_client.ping() is True
