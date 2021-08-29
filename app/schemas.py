from pydantic.main import BaseModel


class Product(BaseModel):
    id: int
    name: str
    CAR: float  # CAR = customer average rating


class TopRatedProductResponse(BaseModel):
    top_product: str
    product_rating: float
