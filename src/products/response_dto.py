from src.products.product import Product


class ResponseDto:

    @staticmethod
    def to_getting(product: Product):
        return {
            "id": product.id,
            "name": product.name,
            "stock": product.stock
        }

    @staticmethod
    def to_listing(product: Product):
        return {
            "id": product.id,
            "name": product.name,
        }
