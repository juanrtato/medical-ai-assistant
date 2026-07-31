from pathlib import Path

from app.core.config import settings
from app.core.logger import logger
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent

PERSIST_DIRECTORY = BASE_DIR / "chroma_db"

vectorstore = Chroma(
    persist_directory=str(PERSIST_DIRECTORY),
    embedding_function=OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY),
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


def retrieve_protocol(query: str):
    """
    Retrieve relevant medical protocols or clinical guidelines based on the provided query.
    This function uses a vector store retriever to perform a semantic search for the query.
    """
    logger.info("[RAG Retriever] Ejecutando búsqueda vectorial para: '%s'", query)
    try:
        docs = retriever.invoke(query)
        logger.info(
            "[RAG Retriever] Se recuperaron %d documentos/fragmentos.", len(docs)
        )
        for idx, doc in enumerate(docs, 1):
            logger.info(
                "[RAG Retriever] Documento %d: %s...",
                idx,
                doc.page_content[:120].replace("\n", " "),
            )

        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        logger.error(
            "[RAG Retriever] Error durante la recuperación RAG para '%s': %s",
            query,
            str(e),
        )
        return f"Error en recuperación RAG: {e!s}"
