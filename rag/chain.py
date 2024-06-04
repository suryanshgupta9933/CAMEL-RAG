# Importing Dependencies
from langchain_openai import ChatOpenAI

# Create the LLM chain
def get_llm_chain(prompt):
    # Create the LLM chain
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.0)
    llm_chain = prompt | llm
    return llm_chain