import os
import tempfile

import streamlit as st

from backend import (
    initialize_rag,
    agent_response
)

st.set_page_config(
    page_title="AgentRAG AI",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:

    st.title("🤖 AgentRAG AI")

    st.markdown("---")

    uploaded_pdf = st.file_uploader(
        "Upload a PDF",
        type="pdf"
    )

    st.markdown("---")

    st.markdown("""
### Features

✅ PDF Question Answering

✅ Live Web Search

✅ Intelligent Routing

✅ LangGraph Workflow

✅ Groq Llama 3.3
""")

st.title("📚 AgentRAG AI")

st.write("Upload a research paper and ask questions.")

if uploaded_pdf:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(uploaded_pdf.read())
        pdf_path = tmp.name

    retriever = initialize_rag(pdf_path)

    question = st.text_input("Ask a question")

    if st.button("Ask Agent"):

        if question:

            with st.spinner("🤖 Thinking..."):

                result = agent_response(
                    question,
                    retriever
                )

            st.markdown("---")

            st.subheader("🧠 Decision")
            st.success(result["decision"])

            st.subheader("✅ Answer")
            st.write(result["answer"])

            st.subheader("📚 Source")
            st.info(result["source"])

        else:
            st.warning("Please enter a question.")