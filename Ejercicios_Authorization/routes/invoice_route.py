from flask import Blueprint, jsonify, request, g

from exceptions.product_exceptions import ProductNotExists, InsufficientStock
from exceptions.invoice_exceptions import InvoiceNotExists

from decorators import require_auth, require_admin


def create_invoice_blueprint(invoice_service, jwt_manager):
    invoice_bp = Blueprint(
        'invoice_bp',
        __name__,
        url_prefix="/invoices"
    )

    #POST - Any authenticated user
    @invoice_bp.route('/purchase', methods=['POST'])
    @require_auth(jwt_manager)
    def purchase_product():
        try:
            data = request.get_json()
            if data.get('product_id') is None or data.get('quantity') is None:
                return {"error": "product_id and quantity are required"}, 400

            #user_id comes from the token, NOT from the request body
            user_id = g.decoded_token["id"]

            invoice = invoice_service.purchase_product(user_id, data.get('product_id'), data.get('quantity'))

            return jsonify(
                id=invoice.id,
                user_id=invoice.user_id,
                product_id=invoice.product_id,
                quantity=invoice.quantity,
                total_price=float(invoice.total_price),
                purchase_date=invoice.purchase_date.isoformat()
            ), 201

        except ProductNotExists as error:
            return {"error": str(error)}, 404
        except InsufficientStock as error:
            return {"error": str(error)}, 400


    #GET - Any authenticated user
    @invoice_bp.route('/me', methods=['GET'])
    @require_auth(jwt_manager)
    def get_my_invoices():

        user_id = g.decoded_token["id"]

        invoices = invoice_service.get_invoices_by_user(user_id)

        return jsonify([
            {
                "id": invoice.id,
                "product_id": invoice.product_id,
                "quantity": invoice.quantity,
                "total_price": float(invoice.total_price),
                "purchase_date": invoice.purchase_date.isoformat()
            }
            for invoice in invoices
        ]), 200


    #DELETE - Admin only
    @invoice_bp.route('/<int:id>', methods=['DELETE'])
    @require_admin(jwt_manager)
    def delete_invoice(id):
        try:
            invoice_service.delete_invoice(id)

            return jsonify(f"The invoice with the ID:{id} has been successfully deleted"), 200

        except InvoiceNotExists as error:
            return {"error": str(error)}, 404


    #PUT - Admin only
    @invoice_bp.route('/<int:id>', methods=['PUT'])
    @require_admin(jwt_manager)
    def update_invoice(id):
        try:
            data = request.get_json()

            updated_invoice = invoice_service.update_invoice(id, data.get('quantity'), data.get('total_price'))

            return jsonify(
                id=updated_invoice.id,
                user_id=updated_invoice.user_id,
                product_id=updated_invoice.product_id,
                quantity=updated_invoice.quantity,
                total_price=float(updated_invoice.total_price),
                purchase_date=updated_invoice.purchase_date.isoformat()
            ), 200

        except InvoiceNotExists as error:
            return {"error": str(error)}, 404


    return invoice_bp
