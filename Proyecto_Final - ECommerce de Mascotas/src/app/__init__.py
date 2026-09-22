from flask import Flask

import app.models  # noqa: F401 - registra todos los modelos en Base.metadata
from app.extensions import Base, SessionLocal, engine
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from app.routes.sales_routes import invoices_bp, sales_bp
from app.utils.errors import register_error_handlers


def create_app():
    app = Flask(__name__)

    Base.metadata.create_all(engine)

    @app.teardown_appcontext
    def remove_db_session(exception=None):
        SessionLocal.remove()

    register_error_handlers(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(invoices_bp)

    return app
