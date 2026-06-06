# Body - Multiple Parameters 
# Mix Path, Query and body parameters

from typing import Annotated

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel , Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# Multiple body parameters- Item and User 
# item key → Item model
# user key → User model

class User(BaseModel):
    username: str
    full_name: str | None = None



async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# Singular Value in Body (Body())
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# Body + Query Together
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

# here 
# item_id → Path
# q → Query
# item, user, importance → Body



# embed=True 

async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results

# FastAPI can handle Path, Query, and Body parameters together.
# A body parameter becomes optional if its default value is None.
# Multiple Pydantic models create a nested JSON body using their parameter names as keys.
# Use Body() for single values (like int, str) that should come from the request body instead of the query.
# Body() also supports validations like gt, ge, lt, and le.
# embed=True wraps a single body parameter inside a JSON key with the parameter's name.
# FastAPI automatically performs type conversion, validation, and API documentation generation




# Body - Fields

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
 

# Field() is used to add validation and metadata inside Pydantic models.
# Import Field from pydantic, not from fastapi.
# It works similarly to Query(), Path(), and Body().
# Common validations:
# gt → greater than
# ge → greater than or equal
# lt → less than
# le → less than or equal
# max_length
# min_length
# Common metadata:
# title
# description
# default
# Field() validations automatically appear in FastAPI's /docs.
# Rule to remember:
# Function parameters → Query(), Path(), Body()
# Pydantic model attributes → Field().





# Body - Nested Models


from pydantic import BaseModel, HttpUrl




# ----------------------
# Nested Model
# ----------------------
class Image(BaseModel):
    url: HttpUrl
    name: str


# ----------------------
# Main Model
# ----------------------
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # List of strings
    categories: list[str] = []

    # Set of strings (duplicates removed)
    tags: set[str] = set()

    # Single nested model
    image: Image | None = None

    # List of nested models
    images: list[Image] | None = None


# ----------------------
# Deeply Nested Model
# ----------------------
class Offer(BaseModel):
    name: str
    description: str | None = None
    items: list[Item]


# =====================================================
# 1. Nested Model + List + Set + List of Nested Models
# =====================================================
@app.post("/items/")
async def create_item(item: Item):
    return item


# =====================================================
# 2. Deeply Nested Model
# =====================================================
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


# =====================================================
# 3. Pure List as Request Body
# =====================================================
@app.post("/images/")
async def create_images(images: list[Image]):
    return images


# =====================================================
# 4. Dictionary Body
# =====================================================
@app.post("/weights/")
async def create_weights(weights: dict[int, float]):
    return weights

# list[str] → List containing strings.
# set[str] → Unique string values (duplicates removed).
# One Pydantic model can contain another model.
# HttpUrl validates URLs automatically.
# You can create lists of nested models (list[Image]).
# Models can be deeply nested (e.g., Offer → Item → Image).
# Request body can also be a pure list (list[Image]).
# You can accept dynamic dictionaries using dict[key_type, value_type].
# FastAPI automatically handles validation, conversion, and API documentation for all nested structures.

