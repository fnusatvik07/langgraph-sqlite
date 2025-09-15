from fastapi import FastAPI, HTTPException
import httpx
from groq import BadRequestError
from langchain_core.messages import HumanMessage

from src.graph import graph
from src.models.schemas import ChatRequest, ChatResponse
from logger.customlogger import CustomLogger


app = FastAPI(title="Langgraph Chatbot- Persistence SQLITE DB", version="1.0.0")
logger=CustomLogger().get_logger(__file__)


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest): 
    
       
    try:
        logger.info(f"Received chat request: thread_id={req.thread_id}, message={req.message}")

        if not req.thread_id or not req.thread_id.strip():
            raise HTTPException(status_code=400, detail="thread_id must not be empty")
        if not req.message or not req.message.strip():
            raise HTTPException(status_code=400, detail="message must not be empty")

        config = {"configurable": {"thread_id": req.thread_id}}

        h_message = HumanMessage(content=req.message)

        response = graph.invoke({"messages": [h_message]}, config)
        logger.info("Graph invocation succeeded")

        latest_ai = response["messages"][-1].content
        logger.info(f"AI Response: {latest_ai}")
        summary = response.get("summary")
        last_messages = [m.content for m in response["messages"]]

        return ChatResponse(reply=latest_ai, summary=summary, last_messages=last_messages)
    except BadRequestError as e:
        logger.exception(f"Groq bad request: {e}")
        raise HTTPException(status_code=400, detail="Invalid model request or parameters")
    except httpx.TimeoutException as e:
        logger.exception(f"Upstream timeout: {e}")
        raise HTTPException(status_code=504, detail="Upstream LLM timeout")
    except Exception as e:
        logger.exception(f"/chat handler failed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
