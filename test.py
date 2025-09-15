from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="Addition API")

# Request Schema

class AddRequest(BaseModel):
    a:float
    b:float

# Response Schema

class AddResponse(BaseModel):
    result:float



@app.post("/add",response_model=AddResponse)
def add(request:AddRequest):
    return {"result": request.a +request.b}

    