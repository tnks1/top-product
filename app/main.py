from app.services import get_highest_rated_product
from app.commons import parse_csv_file
from app.schemas import TopRatedProductResponse
from fastapi import FastAPI, HTTPException, UploadFile, File

app = FastAPI()
t = 'dd'


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
async def create_file(file: UploadFile = File(...)) -> TopRatedProductResponse:
    try:
        # convert sent file a utf-8 encoding string
        file_content = str(file.file.read(), 'utf-8')
        # parse string to a list of object
        parsed_products = await parse_csv_file(file_content)
        # get the highest top product from parsed list
        highest_product = await get_highest_rated_product(parsed_products)
        return {"top_product": str(highest_product.name), "product_rating": highest_product.CAR}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
