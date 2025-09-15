from langchain_core.messages import HumanMessage, RemoveMessage

from logger.customlogger import CustomLogger
from prompt.summary_prompt import build_summary_prompt
from src.models.state import State
from utils.llm import get_chat_model


logger = CustomLogger().get_logger(__file__)
_llm = get_chat_model()


def summary(state: State) -> State:
    try:
        existing_summary = state.get("summary")
        system_prompt = build_summary_prompt(existing_summary)

        message_list = state["messages"] + [HumanMessage(content=system_prompt)]
        logger.info("Invoking Groq LLM for summary node")

        response = _llm.invoke(message_list)
        logger.info("Summary node received response from LLM")

        deleted_messages = [RemoveMessage(m.id) for m in state["messages"][:-2]]

        return {
            "messages": deleted_messages,
            "summary": response.content,
        }
    except Exception as e:
        logger.exception(f"summary node failed: {e}")
        raise
