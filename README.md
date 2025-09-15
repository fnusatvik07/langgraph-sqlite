# LangGraph + SQLite (Modular Structure)

## Folder structure
```
langgraph-sqlite/
  config/
    __init__.py
    settings.py            # env loading and app settings (DB path, model, etc.)
  database/                # sqlite db files
    langgraphchat.db*
  exception/
    __init__.py
    errors.py              # custom exceptions (placeholders no error implemented)
  logger/
    __init__.py
    customlogger.py        # logger 
  prompt/
    __init__.py
    chatbot_prompt.py      # system prompt builder for chatbot
    summary_prompt.py      # system prompt builder for summaries
  src/
    __init__.py
    chatbot.py             # chatbot node
    summary.py             # summary node
    graph.py               # graph assembly and sqlite checkpointer
    main.py                # FastAPI app (entry: src.main:app)
    models/
      __init__.py
      schemas.py           # ChatRequest, ChatResponse
      state.py             # State TypedDict used by the graph
    
  utils/
    __init__.py
    llm.py                 # Groq LLM factory (ChatGroq)
  Dockerfile
  requirements.txt           # deps (langchain, langgraph, langchain-groq,fastapi, ...)
  setup.py
  test.py
  README.md
```