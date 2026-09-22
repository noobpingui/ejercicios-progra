from collections import defaultdict

from app.extensions import SessionLocal
from app.models.cart import CartStatusEnum
from app.models.invoice import InvoiceStatusEnum
from app.models.product import ProductStatusEnum
from app.repositories.cart_repository import CartRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.return_repository import ReturnRepository
from app.utils import cache
from app.utils.errors import ConflictError, NotFoundError, ValidationError
from app.utils.unit_of_work import UnitOfWork

INVOICE_CACHE_KEY_TEMPLATE = "invoice:{}"
INVOICE_CACHE_TTL_SECONDS = 30 * 60


def serialize_invoice(invoice):
    return {
        "invoice_number": str(invoice.invoice_number),
        "user_id": str(invoice.user_id),
        "status": invoice.status.value,
        "billing_address": {
            "street": invoice.billing_street,
            "city": invoice.billing_city,
            "postal_code": invoice.billing_postal_code,
            "country": invoice.billing_country,
        },
        "payment_method": invoice.payment_method,
        "created_at": invoice.created_at.isoformat(),
        "items": [
            {
                "invoice_item_id": str(item.invoice_item_id),
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "price_at_purchase": str(item.price_at_purchase),
            }
            for item in invoice.items
        ],
    }


def create_cart(user_id):
    with UnitOfWork(SessionLocal) as uow:
        cart = CartRepository(uow.session).create(user_id)
        uow.commit()
        # Fuerza la carga de la relación "items" (vacía) mientras la sesión sigue
        # abierta — un carrito recién creado nunca puede tener items todavia, pero
        # la colección queda como lazy-load por default y accederla despues de que
        # el UnitOfWork cierre la sesion lanzaría DetachedInstanceError.
        list(cart.items)
        return cart


def list_pending_carts(user_id):
    session = SessionLocal()
    return CartRepository(session).list_pending_by_user(user_id)


def add_item(cart_id, user_id, product_id, quantity):
    with UnitOfWork(SessionLocal) as uow:
        cart_repo = CartRepository(uow.session)
        cart = cart_repo.get_owned_cart(cart_id, user_id)

        if cart is None:
            raise NotFoundError("Cart not found")

        if cart.status != CartStatusEnum.pending:
            raise ConflictError("Cannot modify a completed cart")

        product = ProductRepository(uow.session).get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if product.status == ProductStatusEnum.inactive:
            raise ValidationError("Cannot add an inactive product")

        item = cart_repo.add_item(cart.cart_id, product_id, quantity)

        uow.commit()
        return item


def update_item_quantity(cart_id, user_id, cart_item_id, quantity):
    with UnitOfWork(SessionLocal) as uow:
        cart_repo = CartRepository(uow.session)
        cart = cart_repo.get_owned_cart(cart_id, user_id)

        if cart is None:
            raise NotFoundError("Cart not found")

        if cart.status != CartStatusEnum.pending:
            raise ConflictError("Cannot modify a completed cart")

        item = cart_repo.get_item(cart.cart_id, cart_item_id)

        if item is None:
            raise NotFoundError("Item not found in cart")

        cart_repo.update_item_quantity(item, quantity)

        uow.commit()
        return item


def remove_item(cart_id, user_id, cart_item_id):
    with UnitOfWork(SessionLocal) as uow:
        cart_repo = CartRepository(uow.session)
        cart = cart_repo.get_owned_cart(cart_id, user_id)

        if cart is None:
            raise NotFoundError("Cart not found")

        if cart.status != CartStatusEnum.pending:
            raise ConflictError("Cannot modify a completed cart")

        item = cart_repo.get_item(cart.cart_id, cart_item_id)

        if item is None:
            raise NotFoundError("Item not found in cart")

        cart_repo.remove_item(item)

        uow.commit()


def checkout(
    cart_id,
    user_id,
    billing_street,
    billing_city,
    billing_postal_code,
    billing_country,
    payment_method,
):
    with UnitOfWork(SessionLocal) as uow:
        cart_repo = CartRepository(uow.session)
        product_repo = ProductRepository(uow.session)
        invoice_repo = InvoiceRepository(uow.session)

        cart = cart_repo.get_owned_cart(cart_id, user_id)

        if cart is None:
            raise NotFoundError("Cart not found")

        if cart.status != CartStatusEnum.pending:
            raise ConflictError("Cart already checked out")

        cart_items = list(cart.items)

        if not cart_items:
            raise ValidationError("Cannot checkout an empty cart")

        # Un mismo producto puede aparecer en mas de un CartItem (add_item no
        # deduplica) — hay que sumar la demanda total por producto ANTES de
        # comparar contra el stock, para no aprobar un checkout que sobrevende
        # un producto repartido en dos líneas del carrito
        requested_quantity_by_product_id = defaultdict(int)
        for item in cart_items:
            requested_quantity_by_product_id[item.product_id] += item.quantity

        # Se bloquean las filas de producto (SELECT ... FOR UPDATE) para cerrar
        # la condicion de carrera entre dos checkouts concurrentes que compiten
        # por el stock del mismo producto .
        # Se recorre en un orden determinístico (por product_id) para que dos
        # checkouts que comparten mas de un producto siempre pidan los locks en
        # el mismo orden entre sí — evita un deadlock cruzado en Postgres.
        products_by_id = {}
        insufficient_products = []
        for product_id, requested_quantity in sorted(
            requested_quantity_by_product_id.items(), key=lambda pair: str(pair[0])
        ):
            product = product_repo.get_for_update(product_id)
            products_by_id[product_id] = product
            if product.stock < requested_quantity:
                insufficient_products.append(product)

        if insufficient_products:
            names = ", ".join(product.name for product in insufficient_products)
            raise ConflictError(f"Insufficient stock for product(s): {names}")

        # Todas las validaciones pasaron — recien ahora se modifica algo
        invoice = invoice_repo.create(
            user_id=user_id,
            billing_street=billing_street,
            billing_city=billing_city,
            billing_postal_code=billing_postal_code,
            billing_country=billing_country,
            payment_method=payment_method,
        )

        for item in cart_items:
            product = products_by_id[item.product_id]
            invoice_repo.add_item(
                invoice,
                product_id=product.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price,
            )
            product_repo.reduce_stock(product, item.quantity)

        cart.status = CartStatusEnum.completed

        uow.commit()

        # Misma coas que en create_cart: forzar la carga de la relacion
        # antes de que el UnitOfWork cierre la sesion.
        list(invoice.items)

        return invoice


def get_invoice(invoice_number, user_id, current_user_role):
    # El owner (user_id) de una Invoice es inmutable una vez creada — a
    # diferencia del status active/inactive de un producto, no puede volverse
    # "mas visible" ni "menos visible" con el tiempo. Por eso es seguro
    # autorizar contra el user_id que trae el propio dato cacheado: la decision
    # de autorizacion sigue corriendo siempre, tanto si el dato sale del cache
    # como de la DB, nunca se devuelve nada sin haberla evaluado antes
    cache_key = INVOICE_CACHE_KEY_TEMPLATE.format(invoice_number)
    cached = cache.get(cache_key)

    if cached is not None:
        if cached["user_id"] != str(user_id) and current_user_role != "admin":
            raise NotFoundError("Invoice not found")
        return cached

    session = SessionLocal()
    invoice = InvoiceRepository(session).get_by_number(invoice_number)

    if invoice is None:
        raise NotFoundError("Invoice not found")

    if invoice.user_id != user_id and current_user_role != "admin":
        raise NotFoundError("Invoice not found")

    serialized = serialize_invoice(invoice)
    cache.set(cache_key, serialized, ttl=INVOICE_CACHE_TTL_SECONDS)

    return serialized


def list_invoices(user_id, current_user_role):
    session = SessionLocal()
    invoice_repo = InvoiceRepository(session)

    if current_user_role == "admin":
        invoices = invoice_repo.list_all()
    else:
        invoices = invoice_repo.list_by_user(user_id)

    return [serialize_invoice(invoice) for invoice in invoices]


def process_return(invoice_number, items):
    with UnitOfWork(SessionLocal) as uow:
        invoice_repo = InvoiceRepository(uow.session)
        product_repo = ProductRepository(uow.session)
        return_repo = ReturnRepository(uow.session)

        invoice = invoice_repo.get_by_number(invoice_number)

        if invoice is None:
            raise NotFoundError("Invoice not found")

        return_ = return_repo.create(invoice_number=invoice.invoice_number)

        # Orden determinístico de locking (mismo criterio que checkout):
        # si dos devoluciones concurrentes comparten líneas de factura, ambas
        # deben pedir los locks en el mismo orden para no deadlockear
        sorted_items = sorted(items, key=lambda entry: str(entry["invoice_item_id"]))

        for entry in sorted_items:
            invoice_item = invoice_repo.get_item_for_update(
                invoice.invoice_number, entry["invoice_item_id"]
            )

            if invoice_item is None:
                raise NotFoundError("Invoice item not found")

            already_returned = return_repo.get_total_returned_quantity(
                invoice_item.invoice_item_id
            )
            available = invoice_item.quantity - already_returned

            if entry["quantity"] > available:
                raise ConflictError(
                    f"Return quantity exceeds available amount ({available}) "
                    f"for invoice item {invoice_item.invoice_item_id}"
                )

            return_repo.add_item(
                return_,
                invoice_item_id=invoice_item.invoice_item_id,
                quantity=entry["quantity"],
            )

            # Mismo lock de fila que en checkout, restaurar stock es otro
            # read-modify-write concurrente que necesita la misma proteccion.
            product = product_repo.get_for_update(invoice_item.product_id)
            product_repo.restore_stock(product, entry["quantity"])

        invoice.status = _compute_invoice_status(invoice, return_repo)

        uow.commit()

        # Misma patron, forzar la carga antes de cerrar la sesion
        list(return_.items)

    cache.invalidate(INVOICE_CACHE_KEY_TEMPLATE.format(invoice_number))

    return return_


def _compute_invoice_status(invoice, return_repo):
    all_items = list(invoice.items)
    any_returned = False
    all_fully_returned = True

    for item in all_items:
        returned = return_repo.get_total_returned_quantity(item.invoice_item_id)
        if returned > 0:
            any_returned = True
        if returned < item.quantity:
            all_fully_returned = False

    if all_fully_returned:
        return InvoiceStatusEnum.fully_returned
    if any_returned:
        return InvoiceStatusEnum.partially_returned
    return InvoiceStatusEnum.completed
