from flask import jsonify, make_response

from src.products.product import Product
from src.products.response_dto import ResponseDto


class ProductsController:

    @staticmethod
    def get_product(product_id):
        product = Product.query.filter_by(id=product_id).first()
        if product is not None:
            return jsonify(ResponseDto.to_getting(product))
        else:
            return make_response(jsonify({}), 404)

    @staticmethod
    def get_products():
        products = Product.query.all()
        return jsonify(products=[ResponseDto.to_listing(p) for p in products])
