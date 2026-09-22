import pytest

from app.utils.errors import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)

EXCEPTIONS = [
    (NotFoundError, 404),
    (ConflictError, 409),
    (ValidationError, 400),
    (ForbiddenError, 403),
    (UnauthorizedError, 401),
]


@pytest.mark.parametrize("exception_cls,status_code", EXCEPTIONS)
def test_error_handler_returns_expected_status_and_format(app, exception_cls, status_code):
    @app.route(f"/__test_raise_{exception_cls.__name__}")
    def _raise():
        raise exception_cls("boom")

    client = app.test_client()
    response = client.get(f"/__test_raise_{exception_cls.__name__}")

    assert response.status_code == status_code
    assert response.get_json() == {"error": "boom"}


def test_unexpected_exception_returns_generic_500(app):
    @app.route("/__test_raise_unexpected")
    def _raise():
        raise RuntimeError("something leaked from a DB driver")

    client = app.test_client()
    response = client.get("/__test_raise_unexpected")

    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal server error"}


def test_unknown_route_still_returns_404(app):
    client = app.test_client()
    response = client.get("/__this_route_does_not_exist")

    assert response.status_code == 404
