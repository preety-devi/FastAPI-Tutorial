from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pydantic import BaseModel

data = {
    "name": "Pen",
    "created_at": datetime.now()
}

encoded_data = jsonable_encoder(data)

print(encoded_data)

#pydantic model

class Item(BaseModel):
    name: str
    price: float


item = Item(name="Book", price=100)

encoded = jsonable_encoder(item)

print(encoded)

#fastapi

app= FastAPI()

@app.get("/items")
async def get_items():
    item = {
        "name": "pen",
        "created_at": datetime.now()
    }
    
    return jsonable_encoder(item)