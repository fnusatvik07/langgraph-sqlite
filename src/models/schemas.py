from pydantic import BaseModel


class ChatRequest(BaseModel):
    thread_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    summary: str | None
    last_messages: list[str]
