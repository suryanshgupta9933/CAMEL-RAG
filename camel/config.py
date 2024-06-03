# Importing Dependencies
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the environment variables
load_dotenv()

# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

# Define roles
assistant_role_name = "Content Writer"
user_role_name = "Founder and CEO"

# Define task
task = "Write a short post on the benefits of using a chatbot on a website."