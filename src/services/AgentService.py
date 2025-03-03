import pandas as pd
from src.core.settings import settings
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_gigachat import GigaChat
from langchain_community.retrievers import BM25Retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.retrievers import EnsembleRetriever

class AgentService:
    async def create_collection(collection_name: str, collection_description: str, file_paths: list):
        documents = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Разбиение текста на чанки

        for file_path in file_paths:
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                pdf_docs = loader.load()
                split_docs = text_splitter.split_documents(pdf_docs)
                documents.extend(split_docs)
            else:
                raise ValueError("Неподдерживаемый формат файла. Поддерживаются только CSV, Excel и PDF файлы.")

        embeddings = HuggingFaceEmbeddings(model_name='deepvk/USER-bge-m3', cache_folder='../cache/embedding/')

        vector_db = Milvus.from_documents(
            documents,
            embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name=collection_name
        )

    async def create_chain_from_existing_collection(system_prompt: str, collection_name: str):

        # Инициализация модели для эмбеддингов
        embeddings = HuggingFaceEmbeddings(model_name='deepvk/USER-bge-m3', cache_folder='../cache/embedding/')

        # Подключение к существующей коллекции Milvus
        vector_db = Milvus(
            embedding_function=embeddings,
            collection_name=collection_name,
            connection_args={"host": "localhost", "port": "19530"}
        )

        # Извлечение документов из коллекции Milvus
        # Предполагаем, что коллекция Milvus содержит поле "page_content" с текстом
        milvus_documents = vector_db.similarity_search(query="", k=1000)  # Извлекаем все документы (или ограниченное количество)

        # Преобразование документов Milvus в формат, подходящий для BM25Retriever
        bm25_documents = [
            Document(page_content=doc.page_content, metadata=doc.metadata) for doc in milvus_documents
        ]

        # Создание BM25Retriever на основе документов из Milvus
        bm25_retriever = BM25Retriever.from_documents(bm25_documents, k=3)  # k — количество возвращаемых документов

        # Создание EnsembleRetriever
        ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_db.as_retriever(), bm25_retriever],
            weights=[0.7, 0.3]  # Веса для каждого ретривера (70% для Milvus, 30% для BM25)
        )

        # Создание цепочки Langchain
        template = system_prompt + "\n\nКонтекст:\n{context}\n\nВопрос: {question}\n\nОтвет:"
        prompt = ChatPromptTemplate.from_template(template)

        # Инициализация GigaChat LLM
        llm = GigaChat(credentials=settings.gigachat_credentials)

        # Создание цепочки
        chain = (
            {"context": ensemble_retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain
