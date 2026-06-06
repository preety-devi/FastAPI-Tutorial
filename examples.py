
from typing import Annotated, Literal
from fastapi import FastAPI, Cookie, Header,status
from pydantic import BaseModel, Field , EmailStr
from fastapi.responses import RedirectResponse, FileResponse ,HTMLResponse , PlainTextResponse

app = FastAPI()

#Header Params

@app.get("/itemsss/")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None
):
    return {"User-Agent" : user_agent}

#Cookie Parameter Models

class Cookies(BaseModel):
    session_id: str = Field(min_length=3)
    theme: str | None = None


@app.get("/items/")
async def read_items(
    cookies: Annotated[Cookies, Cookie()]
):
    return cookies

#Header Param Models

class CommonHeaders(BaseModel):
    host: str
    user_agent: str
    accept: str | None = None
    save_data : bool

@app.get("/items/")
async def read_items(
    headers: Annotated[
        CommonHeaders,
        Header()
    ]
):
    return headers

#Response Model - Return Type

class Student(BaseModel):
    name: str
    semester: int


@app.get("/student/")
async def get_student() -> Student:
    return {
        "name": "Sandhu",
        "semester": 5
    }

class StudentCreate(BaseModel):
    name: str
    email: str
    password: str


class StudentResponse(BaseModel):
    name: str
    email: str

@app.post(
    "/students/",
    response_model=StudentResponse
)
async def create_student(
    student: StudentCreate
):
    return student

class BaseUser(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseUser):
    password: str

@app.post("/register/")
async def register(user: UserCreate) -> BaseUser:
    return user

#Other return type annotations

@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")

@app.get("/download")
async def download() -> FileResponse:
    return FileResponse("report.pdf")

@app.get("/")
async def home() -> HTMLResponse:
    return HTMLResponse(
        "<h1>Hello FastAPI</h1>"
    )

@app.get("/")
async def root() -> PlainTextResponse:
    return PlainTextResponse(
        "Hello World"
    )

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> dict | RedirectResponse:
    if teleport:
        return RedirectResponse(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

    return {"message": "Here's your interdimensional portal."}

#Response Model Encoding Parameters

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]

#Extra Model

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

#Status Codes 

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

@app.post(
    "/userss/",
    status_code=status.HTTP_201_CREATED
)
async def create_user():
    return {"message": "User created"}