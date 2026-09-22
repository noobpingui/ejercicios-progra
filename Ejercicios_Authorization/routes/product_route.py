from flask import Blueprint, jsonify, request

from models.product import Product
from exceptions.product_exceptions import DuplicatedProductName, ProductNotExists, ProductInUse

from decorators import require_admin

from pydantic import ValidationError
from schemas.product_schema import ProductCreate, ProductUpdate


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
            validated_data = ProductCreate.model_validate(data)

            new_product = Product(name=validated_data.name,
                                  price=validated_data.price,
                                  quantity=validated_data.quantity)

            product = product_service.create_product(new_product)

            return jsonify(
                id=product.id,
                name=product.name,
                price=float(product.price),
                quantity=product.quantity
            ), 201

        except ValidationError as error:
            return {"error": error.errors()}, 400 #error.errors() provides a list for each field with the information about what failed and why, instead of a 500 with no context

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

            product_service.delete_product(id)

            return jsonify(f"The product with the ID:{id} has been successfully deleted"), 200

        except ProductInUse as error:
            return {"error": str(error)}, 409

        except ProductNotExists as error:
            return {"error": str(error)}, 404


    #PUT
    @product_bp.route('/<int:id>', methods=['PUT'])
    @require_admin(jwt_manager)
    def update_product(id):
        try:
            data = request.get_json()

            validated_data = ProductUpdate.model_validate(data)

            updated_product = product_service.update_product(id, validated_data.name, validated_data.price, validated_data.quantity)

            return jsonify(
                id=updated_product.id,
                name=updated_product.name,
                price=float(updated_product.price),
                quantity=updated_product.quantity
            ), 200

        except ValidationError as error:
            return {"error": error.errors()}, 400 #error.errors() provides a list for each field with the information about what failed and why, instead of a 500 with no context
        
        except ProductNotExists as error:
            return {"error": str(error)}, 404


    return product_bp
