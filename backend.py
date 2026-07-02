# ==========================================================
# AgentRAG AI Backend
# ==========================================================

import os

from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# ----------------------------
# LLM
# ----------------------------

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ----------------------------
# PDF Loading
# ----------------------------

from langchain_community.document_loaders import PyPDFLoader

# ----------------------------
# Text Splitter
# ----------------------------

from langchain_text_splitters import RecursiveCharacterTextSplitter

# ----------------------------
# Embeddings
# ----------------------------

from langchain_huggingface import HuggingFaceEmbeddings

# ----------------------------
# FAISS
# ----------------------------

from langchain_community.vectorstores import FAISS

# ----------------------------
# Prompt
# ----------------------------

from langchain_core.prompts import ChatPromptTemplate

# ----------------------------
# Parser
# ----------------------------

from langchain_core.output_parsers import StrOutputParser

# ----------------------------
# Tavily
# ----------------------------

from langchain_community.tools.tavily_search import TavilySearchResults

# ----------------------------
# LangGraph
# ----------------------------

from langgraph.graph import StateGraph, END

from typing import TypedDict
# ==========================================================
# Load PDF and Build Vector Database
# ==========================================================

def initialize_rag(pdf_path):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k":5}
    )

    return retriever
# ==========================================================
# Prompt
# ==========================================================

prompt = ChatPromptTemplate.from_template("""
You are an AI Research Assistant.

Answer ONLY using the provided context.

If the answer is not available, reply:

"I could not find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
""")

parser = StrOutputParser()
# ==========================================================
# PDF Tool
# ==========================================================

def pdf_tool(question, retriever):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    chain = prompt | llm | parser

    answer = chain.invoke({
        "context": context,
        "question": question
    })

    pages = sorted(
        set(doc.metadata["page"] + 1 for doc in docs)
    )

    return {
        "answer": answer,
        "source": f"PDF (Pages: {', '.join(map(str,pages))})"
    }
# ==========================================================
# Tavily Web Search
# ==========================================================

web_search = TavilySearchResults(
    max_results=3
)


def web_tool(question):

    results = web_search.invoke(question)

    context = "\n\n".join(
        result["content"]
        for result in results
    )

    answer = llm.invoke(
        f"""
Answer the following question ONLY using the web search results.

Question:
{question}

Search Results:
{context}
"""
    )

    return {
        "answer": answer.content,
        "source": "Live Web Search (Tavily)"
    }
# ==========================================================
# Intelligent Router
# ==========================================================

def router(question, retriever):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    decision_prompt = f"""
You are an intelligent routing agent.

Determine whether the uploaded PDF contains enough information to answer the user's question.

If the PDF contains sufficient information, reply ONLY:

PDF

Otherwise reply ONLY:

WEB

Question:
{question}

Retrieved Context:
{context}
"""

    decision = (
        llm.invoke(decision_prompt)
        .content
        .strip()
        .upper()
    )

    return decision
# ==========================================================
# LangGraph State
# ==========================================================

class AgentState(TypedDict):

    question: str
    retriever: object
    decision: str
    answer: str
    source: str

# ==========================================================
# Router Node
# ==========================================================

def router_node(state):

    question = state["question"]

    decision = router(
        question,
        state["retriever"]
    )

    return {
        "question": question,
        "retriever": state["retriever"],
        "decision": decision
    }
# ==========================================================
# PDF Node
# ==========================================================

def pdf_node(state):

    result = pdf_tool(
        state["question"],
        state["retriever"]
    )

    return {
        "question": state["question"],
        "retriever": state["retriever"],
        "decision": "PDF",
        "answer": result["answer"],
        "source": result["source"]
    }
# ==========================================================
# Web Node
# ==========================================================

def web_node(state):

    result = web_tool(state["question"])

    return {
        "question": state["question"],
        "retriever": state["retriever"],
        "decision": "WEB",
        "answer": result["answer"],
        "source": result["source"]
    }
# ==========================================================
# Build LangGraph
# ==========================================================

workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("pdf", pdf_node)
workflow.add_node("web", web_node)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    lambda state: state["decision"],
    {
        "PDF": "pdf",
        "WEB": "web"
    }
)

workflow.add_edge("pdf", END)
workflow.add_edge("web", END)

graph = workflow.compile()

# ==========================================================
# Agent Response
# ==========================================================

def agent_response(question, retriever):

    result = graph.invoke({
        "question": question,
        "retriever": retriever
    })

    return {
        "question": question,
        "decision": result["decision"],
        "answer": result["answer"],
        "source": result["source"]
    }

