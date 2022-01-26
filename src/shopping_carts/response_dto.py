from src.shared.models import ShoppingCart


class ResponseDto:

    @staticmethod
    def to_creating(shopping_cart: ShoppingCart):
        return {"id": shopping_cart.id}
