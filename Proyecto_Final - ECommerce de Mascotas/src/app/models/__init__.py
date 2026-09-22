# Se importan todos los módulos de modelos para que queden registrados en
# Base.metadata antes de que create_app() llame a Base.metadata.create_all(engine).
from app.models import cart, invoice, product, return_, user  # noqa: F401
