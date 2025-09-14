from dotenv import load_dotenv
from langgraph.graph import START,END,StateGraph
from langchain_anthropic import ChatAnthropic
import sqlite3
import json 
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,RemoveMessage
from chatbot import chatbot
from summary import summary
from state import State
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

# Step 1: Create State - Done

# Step 2: Initialize StateGraph

builder=StateGraph(State)

# Step 3: Initialize LLM

llm=ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0,
    max_tokens=2000,
    timeout=None,
    max_retries=2
)

# Step 4: Create Chatbot Node
# Step 5: Create Summary Node
# Step 6: Create conditional Node

def should_continue(state:State)->str:
    messages=state.get("messages")

    if len(messages)>6:
        return "summary"
    return END

# Step 6: Build Graph

# Add Nodes to the Graph

builder.add_node("llmchat",chatbot)
builder.add_node("summary",summary)

# Add Edges

builder.add_edge(START,"llmchat")
builder.add_conditional_edges("llmchat",should_continue)
builder.add_edge("summary",END)

# Step 7: Compile the Graph with Memory

conn=sqlite3.connect('langgraphchat.db',check_same_thread=False)

memory=SqliteSaver(conn)

graph=builder.compile(checkpointer=memory)

# Step 8: Print the Graph

# Create Chatbot

config={"configurable": {"thread_id": "2"}}

print("Chatbot is Ready. Type exit to quit")

while True:
    user_input=input("Enter Your Question: ")

    if user_input.lower() in ["exit","quit","bye"]:
        print("Good Bye")
        break 
    
    h_message=HumanMessage(content=user_input)
    response=graph.invoke({"messages":[h_message]},config)
    
    # Latest AI Reply

    print("Bot: ", response["messages"][-1].content)

    # Generate Latest Summary

    print(" Current Summary")
    print(response.get("summary","No Summary Yet"))

    print(response)















