from typing import Annotated
from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    if username == "sandhu" and password == "123456":
        return {
            "message": "Login successful"
        }

    return {
        "message": "Invalid credentials"
    }

@app.post("/student-login/")
async def student_login(
    student_id: Annotated[str, Form()],
    password: Annotated[str,Form()]
):
    return {
        "student_id": student_id,
        "message": "Login successful"
    }

#Form_Models

class StudentLogin(BaseModel):
    student_id: str
    password: str

@app.post("/students-login/")
async def student_login(
    data : Annotated[StudentLogin,Form()]
):
    return{
        "student_id": data.student_id,
        "message": "Login successful"
    }