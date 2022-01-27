from src.shared.global_db import GlobalDB
from src.shared.models import ShoppingCart, Product


class ResponseDto:

    @staticmethod
    def to_creating(cart: ShoppingCart):
        return {"id": cart.id}

    @staticmethod
    def show_cart_with_items(cart: ShoppingCart):
        items = []
        for p in cart.products:
            product = GlobalDB.instance().db.session.query(Product) \
                .filter(Product.id == p.product_id).first()
            items.append(
                {
                    "product_id": p.product_id,
                    "name": product.name,
                    "quantity": p.quantity
                }
            )
        return {
            "id": cart.id,
            "items": items
        }
