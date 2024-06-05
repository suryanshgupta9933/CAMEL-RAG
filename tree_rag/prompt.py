# Importing Dependencies
from langchain_core.prompts import ChatPromptTemplate

def get_entity_retriever_prompt():
    # Custom prompt template
    custom_prompt =f"""Identify key entities in the given text and return them back in a list.
    Below is an example of the input and output format:
    User Insights: I want to explore renewable energy sources like solar and wind power, as well as energy storage technologies.
    I'm particularly interested in their cost-effectiveness
    Output: ['renewable energy sources', 'solar power', 'wind power', 'energy storage technologies', 'cost-effectiveness']
    Now we start with the job. Perform the task on given user insights."""
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                custom_prompt,
            ),
            ("human", "User Insights: {user_insights}\nOutput:"),
        ]
    )

    return prompt

def get_search_terms_retriever_prompt():
    # Custom prompt template
    custom_prompt =f"""You will be given a list with key entities. Your task is to mix and match these entities to create relevant google search topic and return them back in a list.
    Below is an example of the input and output format:
    Key entities: ['renewable energy sources', 'solar power', 'wind power', 'energy storage technologies', 'cost-effectiveness']
    Output: ['cost-effectiveness of wind power', 'solar power and energy storage technologies', 'renewable energy sources and solar power']
    Now we start with the job. Perform the task on given key entities."""
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                custom_prompt,
            ),
            ("human", "Key entities: {key_entities}\nOutput:"),
        ]
    )

    return prompt