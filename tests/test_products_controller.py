from flask import json

from app import app, db
from src.products.product import Product


def test_should_return_success_with_an_existing_product_id():
    tmp_product = Product(name="PRODUTO X", stock=5)
    db.session.add(tmp_product)
    db.session.commit()
    response = app.test_client().get(
        f'/products/{tmp_product.id}',
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['id'] == tmp_product.id
    assert data['name'] == tmp_product.name
    assert data['stock'] == tmp_product.stock

    db.session.delete(tmp_product)
    db.session.commit()


def test_should_return_404_with_product_not_exists():
    response = app.test_client().get(
        f'/products/GHOST',
        content_type='application/json',
    )

    assert response.status_code == 404


def test_should_return_list_of_products():
    response = app.test_client().get(
        '/products',
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert type(data['products']) is list
