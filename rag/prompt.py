# Importing Dependencies
from langchain_core.prompts import ChatPromptTemplate

# Return the custom prompt template
def get_custom_prompt_template(assistant_role_name, user_role_name, context):
    # Custom prompt template
    custom_prompt =f"""You are a {assistant_role_name}. Your role is to provide assistance to {user_role_name} in completing the task. 
    You can refer to the context below to generate a response to the user's task and respond with your expertise.
    Contex: {context}
    You are excellent at writing plagrism free content with 100% human-like writing skills and SEO optimized content for improved search engine visiibility.
    """.format(assistant_role_name=assistant_role_name, user_role_name=user_role_name, context=context)
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                custom_prompt,
            ),
            ("human", "Task: {specified_task} \n\n Response:"),
        ]
    )

    return prompt