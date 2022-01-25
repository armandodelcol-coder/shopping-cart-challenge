from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Product %r>' % self.name
