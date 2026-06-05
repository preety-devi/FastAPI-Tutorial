# Path Parameters and Numeric Validations
# Path()
from typing import Annotated
from fastapi import FastAPI, Path , Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="Item ID")]
):
    return {"item_id": item_id}

# Declare metadata
# You can declare all the same parameters as for Query
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number validations
# greater than or equa
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# greater than and less than or equal
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# floats, greater than and less than
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results


# | Validation | Meaning                  |
# | ---------- | ---------------------    |
# | gt         | Greater than             |
# | ge         | Greater than or equal to |
# | lt         | Less than                |
# | le         | Less than or equal to    |


