import os

from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from src.products.products_controller import ProductsController

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    return ProductsController.get_product(product_id)


@app.route('/products', methods=['GET'])
def get_products():
    return ProductsController.get_products()
