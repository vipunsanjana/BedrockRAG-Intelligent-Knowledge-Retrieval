import time
import boto3
import streamlit as st
from botocore.exceptions import ClientError
from langchain_aws import BedrockEmbeddings, ChatBedrockConverse
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# -----------------------------
# Streamlit Setup
# -----------------------------
st.set_page_config(page_title="RAG Bedrock Demo")
st.title("📄 RAG with AWS Bedrock Demo")

# -----------------------------
# AWS Bedrock Clients
# -----------------------------
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Embeddings
bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    client=bedrock_client
)

# LLM - Changed to ChatBedrockConverse for Jamba 1.5 Compatibility
rag_llm = ChatBedrockConverse(
    model_id="ai21.jamba-1-5-mini-v1:0",
    client=bedrock_client,
    temperature=0.7
)

# -----------------------------
# Chat Prompt Template
# -----------------------------
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant. Answer using the provided context. "
        "Summarize in at least 250 words.\n\n"
        "Context:\n{context}"
    ),
    HumanMessagePromptTemplate.from_template("{user_text}")
])

# -----------------------------
# PDF Loading & Splitting
# -----------------------------
def load_documents():
    loader = PyPDFDirectoryLoader("data")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
    return splitter.split_documents(docs)

# -----------------------------
# FAISS Vector Store
# -----------------------------
def create_vectorstore(docs):
    vectorstore = FAISS.from_documents(docs, bedrock_embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

def load_vectorstore():
    return FAISS.load_local(
        "faiss_index",
        embeddings=bedrock_embeddings,
        allow_dangerous_deserialization=True
    )

# -----------------------------
# Helper Functions
# -----------------------------
def safe_generate(llm, messages, retries=5, delay=1.0):
    """Call the LLM safely with retries on throttling"""
    for i in range(retries):
        try:
            # Use .invoke() for ChatBedrockConverse
            result = llm.invoke(messages)
            return result.content
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                wait = delay * (2 ** i)
                st.warning(f"Throttled by Bedrock. Retrying in {wait:.1f} seconds...")
                time.sleep(wait)
            else:
                raise e
    raise Exception("Maximum retries exceeded due to Bedrock throttling.")

def get_answer(user_text, vectorstore):
    # 1. Retrieve top-k relevant documents
    docs = vectorstore.similarity_search(user_text, k=3)
    context_text = "\n\n".join([doc.page_content for doc in docs])

    # 2. Format the Chat Prompt Template
    formatted_messages = chat_prompt.format_messages(
        context=context_text,
        user_text=user_text
    )

    # 3. Call LLM safely
    answer_text = safe_generate(rag_llm, formatted_messages)
    return answer_text

# -----------------------------
# Streamlit Sidebar
# -----------------------------
with st.sidebar:
    st.header("📂 Vector Store Options")
    if st.button("Create/Update Vector Store"):
        with st.spinner("Processing PDFs and creating vector store..."):
            try:
                docs = load_documents()
                if not docs:
                    st.error("No PDFs found in the 'data' folder.")
                else:
                    create_vectorstore(docs)
                    st.success("Vector store created successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# -----------------------------
# User Input
# -----------------------------
user_question = st.text_input("Ask a question from the PDFs:")

if st.button("Get Answer"):
    if not user_question:
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Fetching answer from Bedrock..."):
            try:
                # Load existing index
                vstore = load_vectorstore()
                answer = get_answer(user_question, vstore)
                st.markdown("### Answer")
                st.write(answer)
            except RuntimeError as e:
                # Handle cases where FAISS index doesn't exist yet
                st.error("Vector store not found. Please create it first from the sidebar.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
