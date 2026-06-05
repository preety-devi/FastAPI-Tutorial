# Query()
from inspect import Parameter
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Annotated = Original datatype + Extra FastAPI information

# Query to Annotated in the q parameter  
# min_length
from fastapi import FastAPI, Query

async def read_items(q: str | None = Query(default=None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Pattern (Regular Expression)


async def read_items(
    q: Annotated[
        str | None,
        Query(pattern="^fixedquery$")
    ] = None
):
    return {"q": q}

# Query as the default value
@app.get("/items/")
async def read_items(
    q: Annotated[str, Query(min_length=3)] = "hello"
):
    return {"q": q}

# Required Query Parameter
async def read_items(
    q: Annotated[str, Query(min_length=3)]
):
    return {"q": q}

# Multiple Query Values

async def read_items(
    q: Annotated[list[str] | None, Query()] = None
):
    return {"q": q}

# Title aur Description
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Search Query",
            description="Search item from database"
        )
    ] = None
):
    return {"q": q}


# Alias
async def read_items(
    q: Annotated[
        str | None,
        Query(alias="item-query")
    ] = None
):
    return {"q": q}


# Deprecated Parameter

async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Hidden Parameter
# Query(include_in_schema=False)

async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
    

# Custom Validation
from pydantic import AfterValidator
def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError(
            'ID should start with "isbn-" or "imdb-"'
        )
    return id

async def read_items(
    id: Annotated[str, AfterValidator(check_valid_id)]
):
    return {"id": id}
