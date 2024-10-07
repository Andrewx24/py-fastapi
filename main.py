from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="Spiced Up API", description="A fun and interactive API with various endpoints")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

items = []

@app.get("/")
async def root():
    return {"message": "Welcome to the Spiced Up API!", "endpoints": ["/items", "/random", "/echo", "/calculate"]}

@app.post("/items")
async def create_item(item: Item):
    items.append(item)
    return {"message": "Item created successfully", "item": item}

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.get("/random")
async def get_random_number(min: int = Query(0, description="Minimum value"), 
                            max: int = Query(100, description="Maximum value")):
    return {"random_number": random.randint(min, max)}

@app.get("/echo/{message}")
async def echo(message: str):
    return {"echo": message}

@app.get("/calculate")
async def calculate(operation: str = Query(..., description="Operation to perform (add, subtract, multiply, divide)"),
                    a: float = Query(..., description="First number"),
                    b: float = Query(..., description="Second number")):
    if operation == "add":
        return {"result": a + b}
    elif operation == "subtract":
        return {"result": a - b}
    elif operation == "multiply":
        return {"result": a * b}
    elif operation == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        return {"result": a / b}
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

@app.get("/greet")
async def greet(name: str = Query(None, description="Your name")):
    if name:
        return {"greeting": f"Hello, {name}! Welcome to the Spiced Up API!"}
    else:
        return {"greeting": "Hello, stranger! Care to tell me your name?"}