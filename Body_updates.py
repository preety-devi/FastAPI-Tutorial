from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None

app = FastAPI()

items = {
    "item1": {
        "name": "Book",
        "description": "Old Book",
        "price": 50,
        "tax":5
    }
}

@app.patch("/itemss/{item_id}")
async def update_item(item_id: str, item: ItemUpdate):
    stored_item = items[item_id]

    if not stored_item:
        return {"error": "Item not found"}

    update_data = item.model_dump(exclude_unset=True)

    stored_item.update(update_data)

    return stored_item

#update replacing with put

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded