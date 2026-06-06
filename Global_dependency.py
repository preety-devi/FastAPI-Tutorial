"""
from fastapi import FastAPI, Depends, HTTPException

def verify_token():
    print("Checking token...")
    # imagine security check here


app = FastAPI(dependencies=[Depends(verify_token)])


@app.get("/items/")
def read_items():
    return ["A", "B", "C"]


@app.get("/users/")
def read_users():
    return ["User1", "User2"]
"""
#=========================================================

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

#Dependency with Yield

def get_db():
    db = "DB Connection Opened"
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db=Depends(get_db)):
    return {"db": db}

#subdependencies with yield

def get_db():
    db = "DB CONNECTED"
    try:
        yield db
    finally:
        print("DB CLOSED")

def get_user(db = Depends(get_db)):
    user = f"user loaded using {db}"
    try:
        yield user
    finally:
        print("USER CLEANUP DONE")

@app.get("/profile/")
def profile(user = Depends(get_user)):
    return {"user": user}

#dependencies with yield and httpException

def get_db():
    db = "DB CONNECTED"

    if not db:
        raise HTTPException(status_code=500, detail="DB not available")

    try:
        yield db
    finally:
        print("DB CLOSED")

#=========================================================================

def get_user(token: str):

    if token != "secret":
        raise HTTPException(status_code=401, detail="Invalid token")

    user = {"name": "Sandhu"}

    try:
        yield user
    finally:
        print("User session ended")

@app.get("/profile/")
def profile(user = Depends(get_user)):
    return user

#==============================================================================

def get_db():
    db = "DB"

    if db is None:
        raise HTTPException(status_code=500, detail="DB missing")

    try:
        yield db
    finally:
        print("DB CLOSED")


def get_user(db = Depends(get_db), token: str = ""):
    if token != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = f"user using {db}"

    try:
        yield user
    finally:
        print("USER CLEANED")

#========================================================================
#Dependencies with yield and except
def get_db():
    db = "DB CONNECTED"

    try:
        yield db

    except Exception as e:
        print("Something went wrong inside dependency:", e)
        raise HTTPException(status_code=500, detail="Dependency failed")

    finally:
        print("DB CLOSED")

#=================================

def get_user(token: str):

    try:
        if token != "secret":
            raise HTTPException(status_code=401, detail="Invalid token")

        user = {"name": "Sandhu"}
        yield user

    except Exception as e:
        print("Auth error:", e)
        raise HTTPException(status_code=500, detail="Auth system failure")

    finally:
        print("User session cleanup")

#Context Manager