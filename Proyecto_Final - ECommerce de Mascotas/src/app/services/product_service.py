from app.extensions import SessionLocal
from app.models.product import ProductStatusEnum
from app.repositories.product_repository import ProductRepository
from app.utils import cache
from app.utils.errors import ConflictError, NotFoundError
from app.utils.unit_of_work import UnitOfWork

PRODUCTS_LIST_CACHE_KEY = "products:list"
PRODUCT_CACHE_KEY_TEMPLATE = "product:{}"
PRODUCTS_CACHE_TTL_SECONDS = 5 * 60


def serialize_product(product):
    return {
        "product_id": str(product.product_id),
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
        "status": product.status.value,
    }


def create_product(name, description, price, stock):
    with UnitOfWork(SessionLocal) as uow:
        product = ProductRepository(uow.session).create(
            name=name, description=description, price=price, stock=stock
        )
        uow.commit()

    cache.invalidate(PRODUCTS_LIST_CACHE_KEY)

    return product


def list_active_products():
    cached = cache.get(PRODUCTS_LIST_CACHE_KEY)
    if cached is not None:
        return cached

    session = SessionLocal()
    products = ProductRepository(session).list_active()
    serialized = [serialize_product(product) for product in products]

    cache.set(PRODUCTS_LIST_CACHE_KEY, serialized, ttl=PRODUCTS_CACHE_TTL_SECONDS)

    return serialized


def get_product(product_id, current_user_role):
    if current_user_role == "admin":
        # Un producto inactive solo lo puede ver un admin. El cache no distingue
        # rol, así que esta consulta NUNCA toca el cache (ni lectura ni
        # escritura) — evita que una respuesta pensada para admin (incluyendo
        # productos inactive) quede servida desde cache a un regular_user.
        return _get_product_bypassing_cache(product_id)

    cache_key = PRODUCT_CACHE_KEY_TEMPLATE.format(product_id)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    session = SessionLocal()
    product = ProductRepository(session).get_by_id(product_id)

    if product is None or product.status == ProductStatusEnum.inactive:
        raise NotFoundError("Product not found")

    serialized = serialize_product(product)
    cache.set(cache_key, serialized, ttl=PRODUCTS_CACHE_TTL_SECONDS)

    return serialized


def _get_product_bypassing_cache(product_id):
    session = SessionLocal()
    product = ProductRepository(session).get_by_id(product_id)

    if product is None:
        raise NotFoundError("Product not found")

    return serialize_product(product)


def update_product(product_id, name=None, description=None, price=None, stock=None):
    with UnitOfWork(SessionLocal) as uow:
        product_repo = ProductRepository(uow.session)
        product = product_repo.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if product.status == ProductStatusEnum.inactive:
            raise ConflictError("Cannot modify an inactive product")

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock

        uow.commit()

    cache.invalidate(PRODUCTS_LIST_CACHE_KEY)
    cache.invalidate(PRODUCT_CACHE_KEY_TEMPLATE.format(product_id))

    return product


def delete_product(product_id):
    with UnitOfWork(SessionLocal) as uow:
        product_repo = ProductRepository(uow.session)
        product = product_repo.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if product.status == ProductStatusEnum.inactive:
            raise ConflictError("Product is already inactive")

        product.status = ProductStatusEnum.inactive

        uow.commit()

    cache.invalidate(PRODUCTS_LIST_CACHE_KEY)
    cache.invalidate(PRODUCT_CACHE_KEY_TEMPLATE.format(product_id))

    return product
