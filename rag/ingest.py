# Importing Dependencies
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank

# Injest all the documents from the web into FAISS vectorstore
def ingest_all(documents):
    # Embed the sentences
    embeddings = OpenAIEmbeddings()
    # Store the embeddings
    db = FAISS.from_documents(documents, embeddings, distance_strategy=DistanceStrategy.COSINE)
    db.save_local("rag/vectorstore/positive")
    return db

# Create the retrieval pipeline
def retrieval_pipeline(db):
    # Create the retriever
    retriever = db.as_retriever(search_kwargs={'k': 10})
    # Creating FlashrankRerank compressor
    compressor = FlashrankRerank()
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, 
                                                            base_retriever=retriever)
    return compression_retriever