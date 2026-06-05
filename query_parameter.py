from fastapi import FastAPI
app = FastAPI()


# Query Parameters
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Required Query Parameters
@app.get("/items/{item_id}")
async def read_item(
    item_id: str,
    needy: str
):
    return {
        "item_id": item_id,
        "needy": needy
    }

# mixed example
@app.get("/items/{item_id}")
async def read_item(
    item_id: str,
    needy: str,
    skip: int = 0,
    limit: int | None = None
):
    return {
        "item_id": item_id,
        "needy": needy,
        "skip": skip,
        "limit": limit
    }

