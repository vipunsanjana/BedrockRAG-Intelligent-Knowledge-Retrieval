import streamlit as st
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# -----------------------------
# Initialize Bedrock Chat LLM
# -----------------------------
llm = ChatBedrockConverse(
    model="ai21.jamba-1-5-mini-v1:0", 
    region_name="us-east-1",
    temperature=0.9,
)

# -----------------------------
# Chat Prompt Template
# -----------------------------
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful chatbot. Respond in {language}."
    ),
    HumanMessagePromptTemplate.from_template("{user_text}")
])

# -----------------------------
# Chatbot function
# -----------------------------
def my_chatbot(language, user_text):
    messages = chat_prompt.format_messages(language=language, user_text=user_text)
    
    # Note: ChatBedrockConverse handles BaseMessage objects directly, 
    # but manual formatting as you did is also fine.
    response = llm.invoke(messages)
    return response

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🤖 Bedrock Chatbot Demo")

language = st.sidebar.selectbox(
    "Language", ["English", "Spanish", "Hindi"]
)

user_text = st.sidebar.text_area(
    "What is your question?",
    max_chars=200
)

if user_text:
    with st.spinner("Thinking..."):
        response = my_chatbot(language, user_text)
        # Fix: Access the .content attribute to display text only
        st.markdown(response.content)
