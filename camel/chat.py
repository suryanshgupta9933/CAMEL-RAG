# Importing Dependencies
import re
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from camel import CAMELAgent
from config import assistant_role_name, user_role_name, task
from prompt import task_specifier_sys_msg, task_specifier_msg, get_sys_msgs

# Create a Task Specifing Agent for Brainstorming
task_specify_agent = CAMELAgent(task_specifier_sys_msg, ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.0))
specified_task_msg = task_specify_agent.step(task_specifier_msg)
specified_task = specified_task_msg.content

# Get System and User Inception Messages
assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task)

# Create an Assistant Agent for Inception
assistant_agent = CAMELAgent(assistant_sys_msg, ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.0))

# Create a User Agent for Inception
user_agent = CAMELAgent(user_sys_msg, ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.0))

# Reset agents
assistant_agent.reset()
user_agent.reset()

# Initialize chats
assistant_msg = HumanMessage(
    content=(
        "Now start to give me instructions one by one. "
        "Only reply with Instruction and Input."
    )
)

# Camel Chat Function
def camel_chat():
    chat_turn_limit, n = 10, 0
    assistant_response =[]
    while n < chat_turn_limit:
        n += 1
        user_ai_msg = user_agent.step(assistant_msg)
        user_msg = HumanMessage(content=user_ai_msg.content)
        
        assistant_ai_msg = assistant_agent.step(user_msg)
        assistant_msg = HumanMessage(content=assistant_ai_msg.content)
        
        assistant_response.append(assistant_msg.content)
        if "<CAMEL_TASK_DONE>" in user_msg.content:
            break

    camel_response = "".join(assistant_response)

    # Regex pattern to remove "Solution:" and "<NEXT_REQUEST>"
    pattern = r"Solution: | <NEXT_REQUEST>"

    # Removing the unwanted parts
    try:
        camel_response = re.sub(pattern, "", camel_response)
    except Exception as e:
        print(e)

    return camel_response