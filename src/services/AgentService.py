import pandas as pd
from typing import BinaryIO
from src.core.settings import settings
from src.db.db import Session
from src.models.agent import Agent
from src.models.collection import Collection
from src.models.agent_collection import AgentCollection
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
from sqlalchemy import select


class AgentService:
    async def create_collection(collection_name: str, input_files: list[BinaryIO]):
        documents = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Разбиение текста на чанки

        for file in input_files:
            if file.name.endswith('.pdf'):
                loader = PyPDFLoader(file)
                pdf_docs = loader.load()
                split_docs = text_splitter.split_documents(pdf_docs)
                documents.extend(split_docs)
            else:
                raise ValueError("Неподдерживаемый формат файла. Поддерживаются только PDF файлы.")

        embeddings = HuggingFaceEmbeddings(model_name='deepvk/USER-bge-m3', cache_folder='../cache/embedding/')

        vector_db = Milvus.from_documents(
            documents,
            embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name=collection_name
        )

        async with Session() as session:
            collection = Collection(collection_name=collection_name)
            session.add(collection)
            await session.commit()


    async def get_answer(agent_name: str, user_question: str):
        async with Session() as session:
            q = select(Collection.collection_name, Agent.agent_prompt).\
                select_from(
                    Agent.join(
                        AgentCollection, Agent.agent_id == AgentCollection.agent_id
                    ).join(
                        Collection, AgentCollection.collection_id == Agent.collection_id
                    )
                ).where(Agent.agent_name == agent_name)

            # Выполняем запрос
            result = await session.execute(q)
            
            embeddings = HuggingFaceEmbeddings(model_name='deepvk/USER-bge-m3', cache_folder='../cache/embedding/')

            vector_db = Milvus(
                embedding_function=embeddings,
                collection_name=result.collection_name,
                connection_args={"host": "localhost", "port": "19530"}
            )
            milvus_documents = vector_db.similarity_search(query="", k=1000)
            bm25_documents = [
                Document(page_content=doc.page_content, metadata=doc.metadata) for doc in milvus_documents
            ]

            bm25_retriever = BM25Retriever.from_documents(bm25_documents, k=3)  # k — количество возвращаемых документов

            ensemble_retriever = EnsembleRetriever(
                retrievers=[vector_db.as_retriever(), bm25_retriever],
                weights=[0.7, 0.3]
            )

            template = Agent.agent_prompt + "\n\nКонтекст:\n{context}\n\nВопрос: {question}\n\nОтвет:"
            prompt = ChatPromptTemplate.from_template(template)

            llm = GigaChat(credentials=settings.gigachat_credentials)

            chain = (
                {"context": ensemble_retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

        return chain.invoke(user_question)
    
    async def create_agent(agent_name: str, agent_prompt: str, collection_name: str):
        async with Session() as session:
            agent = Agent(agent_name=agent_name, agent_prompt=agent_prompt)
            q = (select(Collection)).where(Collection.collection_name == collection_name)
            result = await session.execute(q)
            collection = result.scalar_one_or_none()
            session.add(agent)
            await session.flush()
            agent_collection = AgentCollection(agent_id=agent.agent_id, collection=collection.collection_id)
            session.add(agent_collection)
            await session.commit()

    async def get_agents():
        async with Session() as session:
            q = select(Agent.agent_name)
            result = await session.execute(q)
            return result

    async def get_collections():
        async with Session() as session:
            q = select(Collection.collection_name)
            result = await session.execute(q)
            return result
