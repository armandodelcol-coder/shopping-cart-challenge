import os

from flask import Flask, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from src.products.products_controller import ProductsController
from src.shared.global_db import GlobalDB
from src.shopping_carts.shopping_carts_controller import ShoppingCartsController

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

GlobalDB.instance().db = db


@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    return ProductsController.get_product(product_id)


@app.route('/products', methods=['GET'])
def get_products():
    return ProductsController.get_products()


@app.route('/shoppingcarts', methods=['POST'])
def create_shopping_cart():
    data = request.get_json()
    return ShoppingCartsController.create(data)


@app.route('/shoppingcarts/<cart_id>', methods=['POST'])
def add_item_in_cart(cart_id):
    data = request.get_json()
    return ShoppingCartsController.add_item(cart_id, data)


@app.route('/shoppingcarts/<cart_id>/<product_id>', methods=['DELETE'])
def remove_item_in_cart(cart_id, product_id):
    return ShoppingCartsController.remove_item(cart_id, product_id)
