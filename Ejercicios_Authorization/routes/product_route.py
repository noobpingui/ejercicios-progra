from flask import Blueprint, jsonify, request, Response

from models.product import Product
from exceptions.product_exceptions import DuplicatedProductName, ProductNotExists

from decorators import require_admin


def create_product_blueprint(product_service, jwt_manager):
    product_bp = Blueprint(
        'product_bp',
        __name__,
        url_prefix="/products"
    )

    #POST
    @product_bp.route('/', methods=['POST'])
    @require_admin(jwt_manager)
    def create_product():
        try:
            data = request.get_json()
            if data.get('name') is None or data.get('price') is None or data.get('quantity') is None:
                return Response(status=400)

            new_product = Product(name=data.get('name'),
                                  price=data.get('price'),
                                  quantity=data.get('quantity'))

            product = product_service.create_product(new_product)

            return jsonify(
                id=product.id,
                name=product.name,
                price=float(product.price),
                quantity=product.quantity
            ), 201

        except DuplicatedProductName as error:
            return {"error": str(error)}, 400


    #GET ALL
    @product_bp.route('/', methods=['GET'])
    @require_admin(jwt_manager)
    def get_all_products():

        products = product_service.get_all_products()

        return jsonify([
            {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "entry_date": product.entry_date.isoformat(),
                "quantity": product.quantity
            }
            for product in products
        ]), 200


    #GET BY ID
    @product_bp.route('/<int:id>', methods=['GET'])
    @require_admin(jwt_manager)
    def get_product_by_id(id):
        try:
            product = product_service.get_product_by_id(id)

            return jsonify(
                id=product.id,
                name=product.name,
                price=float(product.price),
                quantity=product.quantity
            ), 200

        except ProductNotExists as error:
            return {"error": str(error)}, 404


    #DELETE
    @product_bp.route('/<int:id>', methods=['DELETE'])
    @require_admin(jwt_manager)
    def delete_product(id):
        try:
            product = product_service.get_product_by_id(id)

            product_service.delete_product(product.id)

            return jsonify(f"The product with the ID:{product.id} has been successfully deleted"), 200

        except ProductNotExists as error:
            return {"error": str(error)}, 404


    #PUT
    @product_bp.route('/<int:id>', methods=['PUT'])
    @require_admin(jwt_manager)
    def update_product(id):
        try:
            data = request.get_json()

            updated_product = product_service.update_product(id, data.get('name'), data.get('price'), data.get('quantity'))

            return jsonify(
                id=updated_product.id,
                name=updated_product.name,
                price=float(updated_product.price),
                quantity=updated_product.quantity
            ), 200

        except ProductNotExists as error:
            return {"error": str(error)}, 404


    return product_bp
