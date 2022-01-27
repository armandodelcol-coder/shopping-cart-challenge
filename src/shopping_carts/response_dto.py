from src.shared.models import ShoppingCart


class ResponseDto:

    @staticmethod
    def to_creating(cart: ShoppingCart):
        return {"id": cart.id}

    @staticmethod
    def show_cart_with_items(cart: ShoppingCart):
        return {
            "id": cart.id,
            "items": cart.show_items()
        }
