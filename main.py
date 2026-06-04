from fastapi import FastAPI
APP = FastAPI()
@APP.get("/")
def read_root():
    return {"message": "Hello World"} 