### Setting up the CAMEL-RAG pipeline
# Importing Dependencies
import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage

from rag import (return_filtered_urls, return_camel_response_doc, return_url_doc, 
                ingest_all, retrieval_pipeline, pretty_print_docs, get_llm_chain,
                get_custom_prompt_template)

# Load the Environment Variables
load_dotenv()
# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

# Get the response from the RAG pipeline
def rag_pipeline_response(assistant_role_name, user_role_name, specified_task):
    # Get the URLs for the specified task
    urls = return_filtered_urls(specified_task)
    # Get the CAMEL response document
    camel_response_doc = return_camel_response_doc()
    # Get the URL document
    url_doc = return_url_doc(urls)
    # Combine the CAMEL response document and URL document
    docs = camel_response_doc + url_doc
    # Injest all the documents from the web into FAISS vectorstore
    db = ingest_all(docs)
    # Create the retrieval pipeline
    retriever = retrieval_pipeline(db)
    # Retrieve the ranked documents
    ranked_docs = retriever.invoke(specified_task)
    # Get the context from the ranked documents
    context = ""
    for doc in ranked_docs:
        context += doc.page_content + "\n\n"
    # Get the custom prompt template
    prompt = get_custom_prompt_template(assistant_role_name, user_role_name, context)
    # Get the LLM chain
    llm_chain = get_llm_chain(prompt)
    # Generate the response
    response = llm_chain.invoke({"specified_task": specified_task})
    
    return response.content