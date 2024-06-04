# Importing Dependencies
import os
from dotenv import load_dotenv

from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

from camel import task_specifier_prompts, inception_prompts, get_specified_task, get_sys_msgs, CAMELAgent, camel_chat

# Load the Environment Variables
load_dotenv()

# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

# Camel Pipeline
def camel_pipeline(assistant_role_name, user_role_name, task):
    # Task Specifier Prompts
    task_specifier_sys_msg, task_specifier_msg = task_specifier_prompts(assistant_role_name, user_role_name, task)
    
    # Inception Prompts
    assistant_inception_prompt, user_inception_prompt = inception_prompts(assistant_role_name, user_role_name, task)
    
    # Get the specified task
    specified_task = get_specified_task(task_specifier_sys_msg, task_specifier_msg)

    # Get System and User Inception Messages
    assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task, assistant_inception_prompt, user_inception_prompt)

    # Create an Assistant Agent for Inception
    assistant_agent = CAMELAgent(assistant_sys_msg, ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.0))

    # Create a User Agent for Inception
    user_agent = CAMELAgent(user_sys_msg, ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.0))

    # Initialize chats
    assistant_msg = HumanMessage(
        content=(
            "Now start to give me instructions one by one. "
            "Only reply with Instruction and Input."
        )
    )

    # Start the Camel Chat
    camel_response = camel_chat(user_agent, assistant_agent, assistant_msg)

    return specified_task, camel_response