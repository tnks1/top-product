from app.schemas import Product
from app import get_highest_rated_product, app
from starlette.testclient import TestClient
import pathlib
import pytest

client = TestClient(app)


def test_get_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}


def test_happy_scenario_route():
    path_to_test_file = str(pathlib.Path(
        __file__).parent.resolve())+'/test_data_happy_scenario.csv'
    response = client.post(
        "/", files={"file": ("filename", open(path_to_test_file, "rb"))})
    assert response.status_code == 200
    assert response.json() == {
        "top_product": "\"Massoub gift card\"",
        "product_rating": 5.0
    }


def test_invalid_columns():
    path_to_test_file = str(pathlib.Path(
        __file__).parent.resolve())+'/test_data_invalid_columns.csv'
    response = client.post(
        "/", files={"file": ("filename", open(path_to_test_file, "rb"))})
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'File is not valid for this end point'}


def test_pasring_pydantic_objects():
    path_to_test_file = str(pathlib.Path(
        __file__).parent.resolve())+'/test_data_pasring_pydantic_objects.csv'
    response = client.post(
        "/", files={"file": ("filename", open(path_to_test_file, "rb"))})
    assert response.status_code == 400
    assert response.json() == {
        'detail': "invalid literal for int() with base 10: 'string not int'"}


@pytest.mark.asyncio
async def test_getting_top_product_algorothem():
    test_data = [
        Product(id=1, name='product 1', CAR=1.0),
        Product(id=2, name='product 2', CAR=3.1),
        Product(id=3, name='product 3', CAR=3.9),
        Product(id=4, name='product 4', CAR=1.5),
        Product(id=5, name='product 5', CAR=5.0),
        Product(id=6, name='product 6', CAR=0.05)
    ]
    top_product = await get_highest_rated_product(test_data)
    assert top_product.id == 5
    assert top_product.name == 'product 5'
    assert top_product.CAR == 5.0
