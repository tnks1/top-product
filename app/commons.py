from app.schemas import Product
from typing import List


async def convert_to_pydantic_object(lst_of_items: List[str]) -> List[Product]:
    """ get a list of items and return a list of product pydantic object. This helps in validating types of provided data 

    Args:
        lst_of_items (List[str]) string in list should be in this format (int, string, float): 123, name of product, rating of product   

    Returns:
        List[Product]: list of product pydantic object
    """
    items_list = []
    for item in lst_of_items:
        splitted_item = item.split(',')
        items_list.append(Product(
            id=int(splitted_item[0]), name=str(splitted_item[1]), CAR=float(splitted_item[2])))
    return items_list


async def parse_csv_file(file_content: str) -> List[Product]:
    """ gets a string of all file content and return all products in the file 

    Args:
        file_content (str): utf-8 encoding string of file content 

    Raises:
        Exception: raises in error that might occure in the validating, converting, and/or parsing process 

    Returns:
        List[Product]: list of product pydantic object
    """
    assert len(file_content) > 0  # validate that the list is not empty
    try:
        # removes any lines and store csv lines in a list
        csv_file_rows = [f.strip() for f in file_content.splitlines()]
        # get the columns of csv file
        columns = str(csv_file_rows[0]).split(',')
        # validating file
        await validate_csv_file(columns)
        csv_file_rows.pop(0)  # remove columns from list of rows
        # convert the row of string to list of Product class
        return await convert_to_pydantic_object(csv_file_rows)
    except Exception as e:
        print(e)
        raise Exception(e)


async def validate_csv_file(columns: List[str]):
    """ checks if provided csv file has columns that suits the business logic 

    Args:
        columns ([string]): get a list of columns in csv file

    Raises:
        Exception: file is not valid for this end point
    """
    try:
        assert columns[0] == "id"
        assert columns[1] == "product_name"
        assert columns[2] == "customer_average_rating"
    except Exception as e:
        raise Exception('File is not valid for this end point')
