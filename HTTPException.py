from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

items = {
    1: "Laptop",
    2: "Mobile"
}


@app.get("/items/{item_id}")
async def get_item(item_id: int):

    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "item": items[item_id]
    }


#example 

@app.post("/login/")
async def login(
    username: str,
    password: str
):

    if username != "sandhu":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if password != "123456":
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    return {
        "message": "Login successful"
    }

#adding custom headers
items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

#Custom Exception handler

class StudentNotFoundException(Exception):
    def __init__(self, student_id):
        self.student_id = student_id


@app.exception_handler(StudentNotFoundException)
async def handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Student {exc.student_id} not found"
        }
    )


@app.get("/students/{student_id}")
async def get_student(student_id: int):

    if student_id != 101:
        raise StudentNotFoundException()

    return {
        "student": "Sandhu"
    }

# RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = []

    for error in exc.errors():
        errors.append({
            "field": error["loc"],
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }
    )

#Reuse FastAPI's exception handlers

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}