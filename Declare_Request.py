# Declare Request Example Data
# Examples are used only for API documentation (/docs).
# model_config -> json_schema_extra adds example for the whole model.
# Field(examples=[]) adds example for a specific field.
# Body(examples=[]) adds example for the request body.
# Body(openapi_examples={}) allows multiple selectable examples in Swagger UI.
# Examples improve API readability but do not affect validation or logic.

# 1. Example in Pydantic Model (model_config)
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Laptop",
                    "price": 50000
                }
            ]
        }
    }


# 2. Example using Field()
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(examples=["Laptop"])
    price: float = Field(examples=[50000])


# 3. Example using Body()

from typing import Annotated
from fastapi import Body

@app.post("/items/")
async def create_item(
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Laptop",
                    "price": 50000
                }
            ]
        )
    ]
):
    return item


# 4. Multiple Examples
Body(
    examples=[
        {
            "name": "Laptop",
            "price": 50000
        },
        {
            "name": "Mobile",
            "price": 20000
        }
    ]
)

# 5. examples in JSON Schema - OpenAPI
# When using any of:

# Path()
# Query()
# Header()
# Cookie()
# Body()
# Form()
# File()
# you can also declare a group of examples with additional information that will be added to their JSON Schemas inside of OpenAPI.
# openapi_examples allows multiple examples with titles and descriptions in Swagger UI.
Body(
    openapi_examples={
        "Laptop": {
            "summary": "Laptop Example",
            "value": {
                "name": "Laptop",
                "price": 50000
            }
        },
        "Mobile": {
            "summary": "Mobile Example",
            "value": {
                "name": "Mobile",
                "price": 20000
            }
        }
    }
)
