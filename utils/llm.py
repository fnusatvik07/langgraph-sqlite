from langchain_groq import ChatGroq

from logger.customlogger import CustomLogger
from config.settings import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
    TIMEOUT,
    MAX_RETRIES,
)


logger = CustomLogger().get_logger(__file__)


def get_chat_model() -> ChatGroq:
    try:
        logger.info(f"Initializing ChatGroq model: {MODEL_NAME}")
        return ChatGroq(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            timeout=TIMEOUT,
            max_retries=MAX_RETRIES,
        )
    except Exception as e:
        logger.exception(f"failed to initialize ChatGroq: {e}")
        raise
