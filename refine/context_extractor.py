from typing import List
from src.GoogleSearchScrapper import GoogleSearchModule
import concurrent.futures
from newspaper import Article
from llama_index import Document
from llama_index.node_parser import SentenceSplitter
from llama_index.ingestion import IngestionPipeline
from llama_index import VectorStoreIndex
import concurrent.futures
from llama_index import Document, StorageContext, VectorStoreIndex, ServiceContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.retrievers import BM25Retriever, BaseRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.response_synthesizers import get_response_synthesizer
import logging
from llama_index.prompts import PromptTemplate
logging.basicConfig(level=logging.INFO)


def extract_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return None


def get_context(topics: List[str], num_of_words, topic):

    googleSearch = GoogleSearchModule(topics)
    result = googleSearch.get_all_urls(topics)

    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = [executor.submit(extract_text, url) for url in result]
        concurrent.futures.wait(futures)
        extracted_text = [future.result() for future in futures]

    documents = []
    for text in extracted_text:

        if text != '' and text != None:
            document = Document()
            document.text = text
            documents.append(document)

    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)

    transformations = [text_splitter]
    pipeline = IngestionPipeline(
        transformations=transformations
    )

    nodes = pipeline.run(documents=documents, show_progress=True)

    # logging.info(f"Number of nodes construcuted : {len(nodes)}")

    class HybridRetriever(BaseRetriever):
        def __init__(self, vector_retriever, bm25_retriever):
            self.vector_retriever = vector_retriever
            self.bm25_retriever = bm25_retriever
            super().__init__()

        def _retrieve(self, query, **kwargs):
            bm25_nodes = self.bm25_retriever.retrieve(query, **kwargs)
            vector_nodes = self.vector_retriever.retrieve(query, **kwargs)

            # combine the two lists of nodes
            all_nodes = []
            node_ids = set()
            for n in bm25_nodes + vector_nodes:
                if n.node.node_id not in node_ids:
                    all_nodes.append(n)
                    node_ids.add(n.node.node_id)
            return all_nodes

    embed_model = OpenAIEmbedding(
        model='text-embedding-ada-002')

    service_context_embedding = ServiceContext.from_defaults(
        embed_model=embed_model)

    storage_context = StorageContext.from_defaults()

    storage_context.docstore.add_documents(nodes)

    # llm = OpenAI(model="gpt-4-1106-preview", temperature=0.7)

    index = VectorStoreIndex(
        nodes, storage_context=storage_context, service_context=service_context_embedding)

    vector_retriever = index.as_retriever(similarity_top_k=4)
    bm25_retriever = BM25Retriever.from_defaults(
        nodes=nodes, similarity_top_k=4)

    hybrid_retriever = HybridRetriever(vector_retriever, bm25_retriever)

    # service_context_llms = ServiceContext.from_defaults(
    #     llm=llm)

    summary_prompt_tmpl = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge,"

        "Give a highly detailed and descriptive summary of the topic : {query_str}"
        f"in {str(num_of_words)} words."
        "Make sure to cover all the aspects of the topic by connecting and interlinking them"
        "Focus on facts and figures. Avoid ambiguous and generic information."
        f"Try to pack as much information as you can in the {str(num_of_words)} word summary."
        "Summary : "
    )

    prompt = PromptTemplate(summary_prompt_tmpl)

    response_synthesizer = get_response_synthesizer(
        response_mode='tree_summarize', summary_template=prompt)

    query_engine_summary = RetrieverQueryEngine.from_args(
        retriever=hybrid_retriever,
        response_synthesizer=response_synthesizer,

    )

    summary = query_engine_summary.query(topic)

    return summary.response
