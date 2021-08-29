
from typing import List
from app.schemas import Product


async def get_highest_rated_product(products: List[Product]) -> Product:
    """ basic algorothem to get the top rated product in a list. It first assigns the top product to the first elemnt in the list and then it compare that item to every other item in the list   

    Args:
        products (List[Product]): 

    Returns:
        Product: top rated product
    """
    assert len(products) > 0
    current_high = products[0]
    for product in products:
        if(product.CAR > current_high.CAR):
            current_high = product
    return current_high
