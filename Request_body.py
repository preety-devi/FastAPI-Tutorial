from pydantic import BaseModel
from fastapi import FastAPI
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item

# model_dump() is a method provided by Pydantic models that returns a dictionary representation of the model's data.

async def create_item(item: Item):

    item_dict = item.model_dump()

    if item.tax is not None:
        price_with_tax = item.price + item.tax

        item_dict.update(
            {"price_with_tax": price_with_tax}
        )

    return item_dict

# Path + Request Body
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item
):
    return {
        "item_id": item_id,
        **item.model_dump()
    }

# Path + Query + Body
async def update_item(
    item_id: int,
    item: Item,
    q: str | None = None
):
    result = {
        "item_id": item_id,
        **item.model_dump()
    }

    if q:
        result.update({"q": q})

    return result

# Golden Rule:
# - Path parameters are in curly braces: /items/{item_id}
# - Query parameters appear after ?: /items/?q=value
# - Pydantic models are used for request bodies