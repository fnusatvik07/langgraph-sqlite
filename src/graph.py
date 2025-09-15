import os
import sqlite3

from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph

from logger.customlogger import CustomLogger
from config.settings import SQLITE_DB_PATH
from src.chatbot import chatbot
from src.models.state import State
from src.summary import summary


logger = CustomLogger().get_logger(__file__)
builder = StateGraph(State)


def should_continue(state: State) -> str:
    messages = state.get("messages")
    if len(messages) > 6:
        return "summary"
    return END


builder.add_node("llmchat", chatbot)
builder.add_node("summary", summary)

builder.add_edge(START, "llmchat")
builder.add_conditional_edges("llmchat", should_continue)
builder.add_edge("summary", END)


try:
    # Ensure the database directory exists
    db_dir = os.path.dirname(SQLITE_DB_PATH) or "."
    os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
    memory = SqliteSaver(conn)

    graph = builder.compile(checkpointer=memory)
    logger.info("Graph compiled successfully with SQLite checkpointer")
except Exception as e:
    logger.exception(f"failed to initialize graph/checkpointer: {e}")
    raise
