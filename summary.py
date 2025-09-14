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

def summary(state:State)-> State:
    summary=state.get("summary")

    if summary:
        sys_msg=f"""Given this conversation summary : {summary}

        Your Task:

        1. Analyze New messages provided to this
        2. Identify key updates in topic, context or user Intent
        3.Integrate these updates with existing summary
        4. Maintain Chronological flow and contextual relvance
        5. Focus on information essantial for conversation continuity

        Generate an Update Summary that maintains clarity and coherence 

        """
    else:

        sys_msg=f"""Analyze the Conversation and create a concise summary that:
 
        1. Captures the main topics and Key points discussed
        2. Preserves essential context and decision made
        3. Notes any unresolved questions or action items
        4. Maintain Chronological flow and contextual relvance
        5. Focus on information essantial for conversation continuity

        Generate an Summary that maintains clarity and coherence 

        """
    message=state["messages"] + [HumanMessage(content=sys_msg)]

    #Summary
    response=llm.invoke(message)

    # Delete first 4 Messages or Keep Last 2 messages

    deleted_messages= [RemoveMessage(m.id) for  m in state["messages"][:-2]]

    return {
        "messages": deleted_messages,
        "summary": response.content
    }





