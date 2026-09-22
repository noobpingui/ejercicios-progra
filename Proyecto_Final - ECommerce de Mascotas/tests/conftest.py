import pytest
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.extensions import Base, SessionLocal, engine
from app.utils import cache

# Importar los modelos para que queden registrados en Base.metadata antes del create_all.
from app.models import cart, invoice, product, return_, user  # noqa: F401


@pytest.fixture()
def app():
    return create_app()


@pytest.fixture(scope="session", autouse=True)
def _tables():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session():
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture(autouse=True)
def _remove_scoped_session():
    # Las funciones de service de solo lectura (list_active_products,
    # get_product, login, list_pending_carts, get_invoice, list_invoices)
    # hacen `session = SessionLocal()` y confían en que Flask cierre esa
    # sesión al final del request (teardown_appcontext). Cuando un test llama
    # al service directamente (sin pasar por app.test_client()), ese teardown
    # nunca dispara, y la transacción queda "idle in transaction" indefinida
    # sobre la sesión scoped-por-thread — acumulada a lo largo de toda la
    # corrida, terminó bloqueando el DROP TABLE del teardown de `_tables`.
    # Simulamos acá lo que Flask haría en producción después de cada request.
    yield
    SessionLocal.remove()


@pytest.fixture(autouse=True)
def _clear_product_cache():
    # Muchos tests insertan/borran productos directo en la DB (sin pasar por
    # product_service), así que no disparan la invalidación de cache. Sin esto,
    # un test podría ver una lista/detalle cacheado por otro test anterior.
    cache.invalidate("products:list")
    cache.invalidate("product:*")
    yield
    cache.invalidate("products:list")
    cache.invalidate("product:*")


@pytest.fixture(autouse=True)
def _clear_invoice_cache():
    # Mismo riesgo que con productos: varios tests crean/leen invoices sin
    # pasar por sales_service (o llaman checkout() directo sin pasar por HTTP),
    # lo que puede dejar cache de una factura contaminando el siguiente test.
    cache.invalidate("invoice:*")
    yield
    cache.invalidate("invoice:*")
