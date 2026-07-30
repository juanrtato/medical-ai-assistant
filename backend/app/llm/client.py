from app.core.config import settings
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model=settings.MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=settings.TEMPERATURE,
)

