# 🤖 AgentRAG AI – Agentic Research Paper Question Answering System

An intelligent **Agentic Retrieval-Augmented Generation (RAG)** application that enables users to upload research papers in PDF format and ask natural language questions. The system retrieves the most relevant document chunks using semantic search and generates context-aware answers using **Groq LLM**.

---

## 🚀 Project Highlights

- 📄 Upload any research paper in PDF format
- 🤖 Ask questions in natural language
- 🧠 Semantic search using HuggingFace Embeddings
- ⚡ Fast retrieval with FAISS Vector Database
- 🔄 Agentic workflow powered by LangGraph
- 💬 Interactive Streamlit web interface
- 📚 Retrieval-Augmented Generation (RAG) pipeline
- 🔒 Secure API key management using `.env`

---

# 🖥️ User Interface

## Home Screen

![Home](assets/home.png)

## Research Paper Q&A

![Chat](assets/chat.png)

---

# 🏗️ System Architecture

```
                 PDF Upload
                     │
                     ▼
             PDF Text Extraction
                     │
                     ▼
               Text Chunking
                     │
                     ▼
     HuggingFace Sentence Embeddings
                     │
                     ▼
          FAISS Vector Database
                     │
                     ▼
        Semantic Document Retrieval
                     │
                     ▼
          LangGraph Agent Workflow
                     │
                     ▼
                Groq LLM
                     │
                     ▼
         Context-Aware Response
```

---

# 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| LLM | Groq |
| Framework | LangChain |
| Agent Framework | LangGraph |
| Vector Database | FAISS |
| Embeddings | HuggingFace Sentence Transformers |
| PDF Processing | PyPDF |
| Environment | Python Dotenv |

---

# 📂 Project Structure

```
AgentRAG-AI
│
├── app.py
├── backend.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── assets/
├── sample_documents/
└── AgentRAG_AI.ipynb
```

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/haiderkhadeeja54-png/AgentRAG-AI.git
```

### Move into the project

```bash
cd AgentRAG-AI
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```text
GROQ_API_KEY=your_groq_api_key

TAVILY_API_KEY=your_tavily_api_key
```

### Run the application

```bash
python -m streamlit run app.py
```

---

# 💡 How It Works

1. Upload a research paper.
2. The PDF is converted into text.
3. Text is split into smaller chunks.
4. HuggingFace creates embeddings.
5. FAISS stores the embeddings.
6. Relevant chunks are retrieved using semantic search.
7. Groq LLM generates context-aware answers.

---

# 🎯 Future Improvements

- Multiple PDF support
- Conversation history
- Source citation highlighting
- Persistent vector database
- Cloud deployment
- Authentication system

---

# 👩‍💻 Author

**Khadeeja Haider**

Computer Science Undergraduate

Passionate about Artificial Intelligence, Generative AI, Machine Learning, and NLP.

---

⭐ If you found this project useful, consider giving it a star!
