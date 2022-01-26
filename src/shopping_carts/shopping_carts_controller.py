from flask import make_response, jsonify

from src.shared.global_db import GlobalDB
from src.shared.models import Product, ShoppingCart, ProductsInShoppingCart
from src.shopping_carts.response_dto import ResponseDto


class ShoppingCartsController:

    @staticmethod
    def create(data):
        if data.get('items') is None:
            return make_response(jsonify({
                'message': 'Deve informar uma lista de items'
            }), 422)
        items = data['items']
        new_shopping_cart = ShoppingCart()
        try:
            for i in items:
                product = GlobalDB.instance().db.session.query(Product)\
                    .filter(Product.id == i['product_id']).first()
                if product is not None:
                    if product.stock < i['quantity']:
                        return make_response(jsonify({
                            'message': f'Estoque não é suficiente para o produto: {product.id}'
                        }), 422)
                    product_in_shopping_cart = ProductsInShoppingCart()
                    product_in_shopping_cart.product_id = product.id
                    product_in_shopping_cart.quantity = i['quantity']
                    new_shopping_cart.products.append(product_in_shopping_cart)
            GlobalDB.instance().db.session.add(new_shopping_cart)
            GlobalDB.instance().db.session.commit()
            return make_response(jsonify(ResponseDto.to_creating(new_shopping_cart)), 201)
        except KeyError as k:
            return make_response(jsonify({
                'message': f'Atributo: {k.args[0]} não informado. Verifique se o item contem product_id e quantity'
            }), 422)
