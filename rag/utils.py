# Importing Dependencies
from langchain_community.document_loaders import TextLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .GoogleSearchScrapper import GoogleSearchModule

# Google Search Module
def return_filtered_urls(task):
    # Create an instance of GoogleSearchModule with the topic you want to search for
    search_module = GoogleSearchModule(task)
    # Get URLs, filtered to exclude certain social media sites
    filtered_urls = search_module.get_url(task)
    
    return filtered_urls

# Camel Chat Document Loader
def return_camel_response_doc():
    # Load the camel response document
    loader = TextLoader(r"D:\AIML\CAMEL-RAG\camel_response.txt")
    documents = loader.load()
    # Split the documents into sentences
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    return docs

# Url Document Loader
def return_url_doc(urls):
    # Load the url document
    loader = WebBaseLoader(urls)
    documents = loader.load()
    # Split the documents into sentences
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, strip_whitespace=True)
    docs = splitter.split_documents(documents)

    return docs

# Pretty Print Documents
def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )