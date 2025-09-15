from pydantic import BaseModel


# Request Schema 

class ChatRequest(BaseModel):
    thread_id: str
    message: str

# Response Schema

class ChatResponse(BaseModel):
    reply: str 
    summary: str | None
    last_messages: list[str]

