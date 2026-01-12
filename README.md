# BedrockRAG – Intelligent Knowledge Retrieval

🚀 **BedrockRAG-Intelligent-Knowledge-Retrieval** is a complete **Retrieval-Augmented Generation (RAG)** system built using **Amazon Bedrock**. It enables 🎯 accurate, 🧠 context-aware AI responses by grounding large language model outputs in your own data.

This project demonstrates how to:

* Build a RAG pipeline using **Amazon Bedrock**
* Index documents using **FAISS** for fast similarity search
* Retrieve relevant context and generate reliable answers
* Deploy interactive applications using **Streamlit**

---

## 📂 Project Structure

```
BedrockRAG-Intelligent-Knowledge-Retrieval/
│
├── data/                # Source documents for ingestion
├── faiss_index/         # Vector index generated from documents
├── venv/                # Python virtual environment
├── bedrock.py           # Streamlit app using Amazon Bedrock
├── rag.py                # RAG pipeline Streamlit app
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── LICENSE
├── .env                 # Environment variables (not committed)
├── .gitignore
```

---

## 🧠 Architecture Overview

1. **Document Ingestion** – Load documents from the `data/` directory
2. **Embedding Generation** – Create vector embeddings using Bedrock models
3. **Vector Storage** – Store embeddings in **FAISS**
4. **Retrieval** – Retrieve relevant chunks based on user queries
5. **Generation** – Generate grounded answers using Amazon Bedrock LLMs
6. **UI** – Interactive interface built with **Streamlit**

---

## 🔐 Prerequisites

* AWS Account
* Python **3.9+**
* Amazon Bedrock access enabled in your AWS region

---

## 👤 Step 1: Create AWS IAM User

1. Log in to the **AWS Management Console**
2. Go to **IAM → Users → Create user**
3. Assign **Programmatic access**
4. Attach required permissions (example):

   * `AmazonBedrockFullAccess`
   * `AmazonS3ReadOnlyAccess` (if using S3 data)
5. Save the **Access Key ID** and **Secret Access Key**

---

## ⚙️ Step 2: Set Up Python Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

* **Windows**

  ```bash
  venv\Scripts\activate
  ```

* **macOS / Linux**

  ```bash
  source venv/bin/activate
  ```

---

## 📦 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ☁️ Step 4: Install & Configure AWS CLI

### Install AWS CLI

Follow the official AWS documentation:

👉 [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Configure AWS Credentials

```bash
aws configure
```

You will be prompted for:

* AWS Access Key ID
* AWS Secret Access Key
* Default region (example: `us-east-1`)
* Output format (json recommended)

---

## 🚀 Step 5: Run the Streamlit Applications

### Run Bedrock App

```bash
streamlit run bedrock.py
```

### Run RAG Application

```bash
streamlit run rag.py
```

The app will be available at:

```
http://localhost:8501
```

---

## 🧪 Use Cases

* Enterprise knowledge base Q&A
* Document search & summarization
* Internal AI assistants
* Research and analysis tools

---

## 🔒 Security Notes

* Never commit AWS credentials to GitHub
* Always use `.env` or AWS CLI configuration
* Follow the principle of least privilege for IAM roles

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

* Amazon Bedrock
* FAISS
* Streamlit
* Python Open Source Community

---

## 👨‍💻 Author

**Vipun Sanjana**  
Software Engineer  
Specialized in DevOps & Generative AI  

🔗 GitHub: https://github.com/vipunsanjana  
🔗 LinkedIn: https://www.linkedin.com/in/vipun/ 
📧 Email: vipunsanjana34@email.com
🌐 Portfolio: https://vipunsanjana.dev

✨ *Build intelligent, reliable AI systems with Bedrock-powered RAG!*
