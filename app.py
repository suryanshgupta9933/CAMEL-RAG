### Streamlit App
# Importing Dependencies
import os
import time
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
    st.title("🐪 CAMEL-RAG Pipeline 🤖")
    st.write("This is a demo of the CAMEL-RAG pipeline. Enter a task for the assistant to perform.")

    st.markdown(f"### Assistant Role: **{assistant_role_name}**")
    st.markdown(f"### User Role: **{user_role_name}**")

    # User input
    user_input = st.text_area("Enter your task here:")
    if st.button("Submit"):
        if user_input.strip() == "":
            st.warning("Please enter a task before submitting.")
        else:
            # Calculate CAMEL pipeline response time
            start_time = time.time()
            with st.spinner("Generating CAMEL response..."):
                try:
                    specified_task, camel_response = camel_pipeline_response(assistant_role_name, user_role_name, user_input)
                except Exception as e:
                    st.error(f"Error generating CAMEL response: {e}")
                    return
            camel_response_time = time.time() - start_time

            # Display the CAMEL response
            st.markdown("## CAMEL Response:")
            st.write(camel_response)
            st.markdown(f"**Response Time:** {camel_response_time:.2f} seconds")

            # Calculate RAG pipeline response time
            start_time = time.time()
            with st.spinner("Generating RAG response..."):
                try:
                    rag_response = rag_pipeline_response(assistant_role_name, user_role_name, specified_task)
                except Exception as e:
                    st.error(f"Error generating RAG response: {e}")
                    return
            rag_response_time = time.time() - start_time

            # Display the RAG response
            st.markdown("## RAG Response:")
            st.write(rag_response)
            st.markdown(f"**Response Time:** {rag_response_time:.2f} seconds")

if __name__ == "__main__":
    app()