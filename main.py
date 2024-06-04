### Setting up the CAMEL-RAG pipeline
# Importing Dependencies
import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage

from camel_pipeline import camel_pipeline
from rag import return_filtered_urls, return_camel_response_doc, return_url_doc, ingest_all, retrieval_pipeline, pretty_print_docs

# Load the Environment Variables
load_dotenv()

# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

# Define the roles and task
assistant_role_name = "Content Writer"
user_role_name = "Founder and CEO"
user_task = "Write a linkedin post about AI in healthcare."

# Run the CAMEL pipeline
specified_task, camel_response = camel_pipeline(assistant_role_name, user_role_name, user_task)

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

# Pretty print the ranked documents
pretty_print_docs(ranked_docs)