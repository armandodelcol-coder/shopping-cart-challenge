import json
import unittest
import uuid

from app import app
from src.shared.global_db import GlobalDB
from src.shared.models import Product, ShoppingCart, ProductsInShoppingCart


class TestShoppingCartController(unittest.TestCase):

    def test_should_create_shopping_cart_with_success(self):
        # PREPARE TEMP DATA
        tmp_product = Product(name="PRODUTO X", stock=5)
        GlobalDB.instance().db.session.add(tmp_product)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            '/shoppingcarts',
            data=json.dumps({
                'items': [
                    {'product_id': tmp_product.id, 'quantity': 3}
                ]
            }),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 201
        assert data['id'] is not None

        # CLEAR TESTS DB
        GlobalDB.instance().db.session.query(ProductsInShoppingCart) \
            .filter(ProductsInShoppingCart.shopping_cart_id == data['id']).delete()
        GlobalDB.instance().db.session.query(ShoppingCart) \
            .filter(ShoppingCart.id == data['id']).delete()
        GlobalDB.instance().db.session.delete(tmp_product)
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()

    def test_should_return_error_with_stock_insufficient(self):
        # PREPARE TEMP DATA
        tmp_product = Product(name="PRODUTO X", stock=5)
        GlobalDB.instance().db.session.add(tmp_product)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            '/shoppingcarts',
            data=json.dumps({
                'items': [
                    {'product_id': tmp_product.id, 'quantity': 10}
                ]
            }),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 422
        assert data['message'] == f'Estoque não é suficiente para o produto: {tmp_product.id}'
        GlobalDB.instance().db.session.delete(tmp_product)
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()

    def test_should_return_error_without_items(self):
        response = app.test_client().post(
            '/shoppingcarts',
            data=json.dumps({}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 422
        assert data['message'] == f'Deve informar uma lista de items'

    def test_should_return_error_with_item_args_invalid(self):
        response = app.test_client().post(
            '/shoppingcarts',
            data=json.dumps({
                'items': [
                    {'fake': '123', 'quantity': 10}
                ]
            }),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 422
        assert data['message'] == 'Atributo: product_id não informado. ' \
                                  'Verifique se o item contem product_id e quantity'

    def test_should_add_item_in_shopping_cart(self):
        # PREPARE TEMP DATA
        tmp_cart = ShoppingCart()
        GlobalDB.instance().db.session.add(tmp_cart)
        tmp_product = Product(name="PRODUTO X", stock=5)
        GlobalDB.instance().db.session.add(tmp_product)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            f'/shoppingcarts/{tmp_cart.id}',
            data=json.dumps({'product_id': tmp_product.id, 'quantity': 1}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert len(data['items']) > 0
        assert data['items'][0]['product_id'] == data['items'][0]['product_id']
        assert data['items'][0]['name'] == data['items'][0]['name']
        assert data['items'][0]['quantity'] == 1

        # CLEAR TESTS DB
        GlobalDB.instance().db.session.query(ProductsInShoppingCart) \
            .filter(ProductsInShoppingCart.shopping_cart_id == data['id']).delete()
        GlobalDB.instance().db.session.delete(tmp_product)
        GlobalDB.instance().db.session.query(ShoppingCart) \
            .filter(ShoppingCart.id == data['id']).delete()
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()

    def test_should_return_404_if_cart_not_found(self):
        response = app.test_client().post(
            f'/shoppingcarts/{uuid.uuid4()}',
            data=json.dumps({'product_id': '123', 'quantity': 1}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 404
        assert data['message'] == 'Carrinho não encontrado'

    def test_should_not_add_item_in_cart_if_stock_insufficient(self):
        # PREPARE TEMP DATA
        tmp_cart = ShoppingCart()
        GlobalDB.instance().db.session.add(tmp_cart)
        tmp_product = Product(name="PRODUTO X", stock=5)
        GlobalDB.instance().db.session.add(tmp_product)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            f'/shoppingcarts/{tmp_cart.id}',
            data=json.dumps({'product_id': tmp_product.id, 'quantity': 6}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 422
        assert data['message'] == f'Estoque não é suficiente para o produto: {tmp_product.id}'

        # CLEAR TESTS DB
        GlobalDB.instance().db.session.delete(tmp_product)
        GlobalDB.instance().db.session.query(ShoppingCart) \
            .filter(ShoppingCart.id == tmp_cart.id).delete()
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()

    def test_should_return_error_if_product_not_found(self):
        # PREPARE TEMP DATA
        product_id = uuid.uuid4()
        tmp_cart = ShoppingCart()
        GlobalDB.instance().db.session.add(tmp_cart)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            f'/shoppingcarts/{tmp_cart.id}',
            data=json.dumps({'product_id': str(product_id), 'quantity': 6}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 422
        assert data['message'] == f'Não foi encontrado o produto com id: {str(product_id)}'

        # CLEAR TESTS DB
        GlobalDB.instance().db.session.query(ShoppingCart) \
            .filter(ShoppingCart.id == tmp_cart.id).delete()
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()

    def test_should_return_error_if_quantity_is_smaller_then_0(self):
        # PREPARE TEMP DATA
        tmp_cart = ShoppingCart()
        GlobalDB.instance().db.session.add(tmp_cart)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            f'/shoppingcarts/{tmp_cart.id}',
            data=json.dumps({'product_id': str(uuid.uuid4()), 'quantity': -1}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 422
        assert data['message'] == f'Quantidade deve ser maior que zero'

        # CLEAR TESTS DB
        GlobalDB.instance().db.session.query(ShoppingCart) \
            .filter(ShoppingCart.id == tmp_cart.id).delete()
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()

    def test_should_sum_quantity_in_shopping_cart_if_item_already_exists(self):
        # PREPARE TEMP DATA
        tmp_cart = ShoppingCart(id=uuid.uuid4())
        GlobalDB.instance().db.session.add(tmp_cart)
        tmp_product = Product(id=uuid.uuid4(), name="PRODUTO X", stock=5)
        GlobalDB.instance().db.session.add(tmp_product)
        product_in_shopping_cart = ProductsInShoppingCart()
        product_in_shopping_cart.product_id = tmp_product.id
        product_in_shopping_cart.quantity = 1
        tmp_cart.products.append(product_in_shopping_cart)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            f'/shoppingcarts/{tmp_cart.id}',
            data=json.dumps({'product_id': tmp_product.id, 'quantity': 1}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert len(data['items']) > 0
        assert data['items'][0]['product_id'] == data['items'][0]['product_id']
        assert data['items'][0]['name'] == data['items'][0]['name']
        assert data['items'][0]['quantity'] == 2

        # CLEAR TESTS DB
        GlobalDB.instance().db.session.query(ProductsInShoppingCart) \
            .filter(ProductsInShoppingCart.shopping_cart_id == data['id']).delete()
        GlobalDB.instance().db.session.delete(tmp_product)
        GlobalDB.instance().db.session.query(ShoppingCart) \
            .filter(ShoppingCart.id == data['id']).delete()
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()

    def test_should_not_add_item_in_cart_if_product_already_exists_and_stock_insufficient(self):
        # PREPARE TEMP DATA
        tmp_cart = ShoppingCart(id=uuid.uuid4())
        GlobalDB.instance().db.session.add(tmp_cart)
        tmp_product = Product(id=uuid.uuid4(), name="PRODUTO X", stock=5)
        GlobalDB.instance().db.session.add(tmp_product)
        product_in_shopping_cart = ProductsInShoppingCart()
        product_in_shopping_cart.product_id = tmp_product.id
        product_in_shopping_cart.quantity = 1
        tmp_cart.products.append(product_in_shopping_cart)
        GlobalDB.instance().db.session.commit()

        response = app.test_client().post(
            f'/shoppingcarts/{tmp_cart.id}',
            data=json.dumps({'product_id': tmp_product.id, 'quantity': 5}),
            content_type='application/json',
        )

        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 422
        assert data['message'] == f'Estoque não é suficiente para o produto: {tmp_product.id}'

        # CLEAR TESTS DB
        GlobalDB.instance().db.session.query(ProductsInShoppingCart) \
            .filter(ProductsInShoppingCart.shopping_cart_id == tmp_cart.id).delete()
        GlobalDB.instance().db.session.delete(tmp_product)
        GlobalDB.instance().db.session.query(ShoppingCart) \
            .filter(ShoppingCart.id == tmp_cart.id).delete()
        GlobalDB.instance().db.session.commit()
        GlobalDB.instance().db.session.close()
