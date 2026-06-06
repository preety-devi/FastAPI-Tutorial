from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


@app.get(
    "/items/",
    summary="Get all items",
    description="This endpoint returns a list of all items in the system",
)
async def get_items():
    return ["pen", "book", "laptop"]

#tags

@app.get("/itemss/", tags=["Items"])
async def get_items():
    return ["pen", "book"]

#responase model

class Item(BaseModel):
    name: str

@app.get("/items/{id}", response_model=Item)
async def get_item(id: int):
    return {"name": "pen", "price": 10}

#status code

@app.post("/itemsss/", status_code=status.HTTP_201_CREATED)
async def create_item():
    return {"message": "created"}

#deprecated = True mark old apis

@app.get("/old-items/",deprecated=True)
async def old_items():
    return["old"]

#response description
@app.get("/itemssss",response_description="List of items retrieved successfully")
async def get_items():
    return ["pen"]

#full example

class Item(BaseModel):
    name: str
    price: float


@app.post(
    "/items/",
    summary="Create a new item",
    description="This API creates a new item in the database",
    tags=["Items"],
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
)
async def create_item():
    return {"name": "Pen", "price": 10, "extra": "ignored"}