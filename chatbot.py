from dotenv import load_dotenv
from langgraph.graph import START,END,StateGraph
from langchain_anthropic import ChatAnthropic
import sqlite3
import json 
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,RemoveMessage
from state import State

load_dotenv()


llm=ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0,
    max_tokens=2000,
    timeout=None,
    max_retries=2
)

def chatbot(state:State)->State:

    summary=state.get("summary")

    if summary:
        sys_msg=f"""
        You are continuing a conversation with a user.
        Here is a concise summary of the conversation so far:

        {summary}
        
        Use this summary as prior context when generating your next response.
        Ensure the Response feel natural, maintains continuity and addresses the user's
        most recent message appropriately

        """
        messages=[SystemMessage(sys_msg)] + state["messages"]

    else:
        sys_msg=f"""

        You are an intelligent conversation chatbot.
        Your task is to generate an approporate followup response based on the conversation provided

        Make sure to:

        1. Understand the full context of messages provided
        2. Maintain tone, style and continuity
        3. Address any question or unresolved points
        4. Keep you response coherent
        
        """

        messages=[SystemMessage(sys_msg)] + state["messages"]

    #LLM Call

    response=llm.invoke(messages)

    return {
        "messages":[AIMessage(content=response.content)]
    }
