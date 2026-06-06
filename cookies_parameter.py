#Cookie Parameters

#  cookie() is used to read cookie values from the request.
# It works similarly to Query() and Path().
# Without Cookie(), FastAPI treats the parameter as a query parameter.
# Supports validation (min_length, max_length, etc.).
# Swagger UI usually cannot send cookies automatically due to browser restrictions.
# Cookies are commonly used for sessions, authentication, and user tracking.

from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


# Cookies Parameter Models

# Use a Pydantic model to group related cookies.
# FastAPI automatically maps cookie values to model fields.
# Makes code cleaner and reusable.
# model_config = {"extra": "forbid"} rejects unknown cookies.
# Same concept works for Query, Cookie, and Header parameter models.
# Available since FastAPI 0.115.0.

# Cookies with a Pydantic Model

# from typing import Annotated

# from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


# @app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies

# Forbid Extra Cookies


class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


# @app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies