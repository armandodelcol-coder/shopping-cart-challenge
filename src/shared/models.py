import decimal
import uuid

from flask_sqlalchemy import SQLAlchemy

from src.shared.global_db import GlobalDB

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name


class ShoppingCart(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True, default=uuid.uuid4)
    products = db.relationship('ProductsInShoppingCart', back_populates='shopping_cart')
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'), nullable=True)

    def show_items(self):
        items = []
        for p in self.products:
            product = GlobalDB.instance().db.session.query(Product) \
                .filter(Product.id == p.product_id).first()
            items.append(
                {
                    "product_id": p.product_id,
                    "name": product.name,
                    "quantity": p.quantity,
                    "price": product.price,
                    "subtotal": decimal.Decimal(
                        product.price * decimal.Decimal(p.quantity)
                    ).quantize(decimal.Decimal('0.01'))
                }
            )
        return items

    def total(self):
        total = decimal.Decimal(0)
        for i in self.show_items():
            total += i['subtotal']
        return total

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


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False)
    discount_percentage = db.Column(db.Numeric(10, 2), nullable=False)
    is_valid = db.Column(db.Boolean, default=False, nullable=False)
