# Query Parameters with a Pydantic Model 
# If you have a group of query parameters that are related, you can create a Pydantic model to declare them.This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once.
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

# Groups multiple related query parameters into one Pydantic model.
# Makes code clean and reusable.
# Uses Field() for validation (gt, ge, lt, le).
# Uses Literal to allow only specific values.
# Supports multiple values with list[str].
# model_config = {"extra": "forbid"} rejects unknown query parameters.
# FastAPI automatically generates validation and API docs (/docs)
