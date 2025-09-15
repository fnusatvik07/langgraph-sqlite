from langchain_core.messages import SystemMessage, AIMessage

from logger.customlogger import CustomLogger
from prompt.chatbot_prompt import build_chatbot_system_prompt
from src.models.state import State
from utils.llm import get_chat_model


logger = CustomLogger().get_logger(__file__)
_llm = get_chat_model()


def chatbot(state: State) -> State:
    try:
        existing_summary = state.get("summary")
        system_prompt = build_chatbot_system_prompt(existing_summary)

        messages = [SystemMessage(system_prompt)] + state["messages"]
        logger.info("Invoking Groq LLM for chatbot node")

        response = _llm.invoke(messages)
        logger.info("Chatbot node received response from LLM")

        return {
            "messages": [AIMessage(content=response.content)],
        }
    except Exception as e:
        logger.exception(f"chatbot node failed: {e}")
        raise
