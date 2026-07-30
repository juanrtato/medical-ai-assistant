from pathlib import Path

from app.core.config import settings
from app.core.logger import logger
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent.parent

PROTOCOLS_PATH = BASE_DIR / "knowledge" / "protocols"

PERSIST_DIRECTORY = BASE_DIR / "chroma_db"


def build_vectorstore():
    logger.info("[RAG Indexer] Cargando protocolos desde %s", PROTOCOLS_PATH)
    loader = DirectoryLoader(
        str(PROTOCOLS_PATH),
        glob="**/*.md",
        loader_cls=TextLoader,
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIRECTORY),
    )

    logger.info(
        "[RAG Indexer] Indexación completada: %d fragmentos guardados en %s.",
        len(chunks),
        PERSIST_DIRECTORY,
    )
    print(f"Indexed {len(chunks)} chunks.")


def ensure_vectorstore_indexed():
    """Verifica si la base de datos ChromaDB existe; si no existe o está vacía, la indexa automáticamente."""
    if not PERSIST_DIRECTORY.exists() or not any(PERSIST_DIRECTORY.iterdir()):
        logger.info(
            "[RAG Indexer] No se encontró la base vectorial. Iniciando auto-indexación de protocolos..."
        )
        try:
            build_vectorstore()
        except Exception as e:
            logger.error("[RAG Indexer] Error durante la auto-indexación: %s", str(e))
    else:
        logger.info(
            "[RAG Indexer] Base vectorial ChromaDB detectada en %s.", PERSIST_DIRECTORY
        )
