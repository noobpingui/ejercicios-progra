from flask import jsonify
from werkzeug.exceptions import HTTPException


class AppError(Exception):
    status_code = 500

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(AppError):
    status_code = 400


class UnauthorizedError(AppError):
    status_code = 401


class ForbiddenError(AppError):
    status_code = 403


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        if isinstance(error, HTTPException):
            return error
        return jsonify({"error": "Internal server error"}), 500
