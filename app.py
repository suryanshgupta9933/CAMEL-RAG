### Streamlit App
import os
import streamlit as st

from camel_pipeline import camel_pipeline_response
from rag_pipeline import rag_pipeline_response

# Define the roles and task
assistant_role_name = "Content Writer"
user_role_name = "Founder and CEO"

# Main Streamlit app
def app():
    # Set page title
    st.set_page_config(page_title="CAMEL-RAG Pipeline",
                        page_icon="🐪",
                        layout="centered")

    # Add a header
    st.title("🐪CAMEL-RAG Pipeline🤖")
    st.write("This is a demo of the CAMEL-RAG pipeline.\n\n")

    st.markdown("### Assitant Role: {}".format(assistant_role_name))
    st.markdown("### User Role: {}".format(user_role_name))

    # User input
    user_input = st.text_area("Enter your task here:")
    if st.button("Submit"):
        # Get the response from the CAMEL pipeline
        specified_task, camel_response = camel_pipeline_response(assistant_role_name, user_role_name, user_input)
        # Display the CAMEL response
        st.markdown("## CAMEL Response:")
        st.write(camel_response)
        # Get the response from the RAG pipeline
        rag_response = rag_pipeline_response(assistant_role_name, user_role_name, specified_task)
        # Display the RAG response
        st.markdown("## RAG Response:")
        st.write(rag_response)

if __name__ == "__main__":
    app()