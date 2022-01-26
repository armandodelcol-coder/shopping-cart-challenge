import uuid

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Product %r>' % self.name


class ShoppingCart(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True, default=uuid.uuid4)
    products = db.relationship('ProductsInShoppingCart', back_populates='shopping_cart')

    def __repr__(self):
        return '<ShoppingCart %r>' % self.id


class ProductsInShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product_id = db.Column('product_id', db.String, db.ForeignKey('product.id'))
    shopping_cart_id = db.Column('shopping_cart_id', db.String, db.ForeignKey('shopping_cart.id'))
    product = db.relationship("Product")
    shopping_cart = db.relationship("ShoppingCart", back_populates="products")

    def __repr__(self):
        return '<ProductsInShoppingCart %r>' % self.id
