
import streamlit as st
import pandas as pd
import tempfile
import os
from rag_pipeline import build_faiss_index, search_metadata
from metadata_indexer import extract_metadata
from llm_answer import answer_question_with_context

st.set_page_config(page_title="Conversational Data Catalog with RAG", layout="wide")
st.title("Conversational Data Catalog with Advanced RAG")

# Session state for metadata and FAISS index
if 'metadata_chunks' not in st.session_state:
    st.session_state['metadata_chunks'] = []
if 'faiss_built' not in st.session_state:
    st.session_state['faiss_built'] = False

st.sidebar.header("Upload Datasets")
uploaded_files = st.sidebar.file_uploader(
    "Upload one or more CSV files", type=["csv"], accept_multiple_files=True
)

if uploaded_files:
    st.session_state['metadata_chunks'] = []
    for uploaded_file in uploaded_files:
        # Save to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        # Extract metadata
        meta = extract_metadata(tmp_path)
        st.session_state['metadata_chunks'].append(meta)
        os.unlink(tmp_path)
    # Build FAISS index for uploaded files
    build_faiss_index(st.session_state['metadata_chunks'])
    st.session_state['faiss_built'] = True
    st.success(f"Indexed {len(uploaded_files)} dataset(s)!")

st.header("Ask Questions about Your Data Catalog")
user_query = st.text_input("Enter your question:")


if user_query and st.session_state.get('faiss_built', False):
    results = search_metadata(user_query)
    st.subheader("Relevant Metadata Chunks:")
    for i, chunk in enumerate(results, 1):
        st.markdown(f"**Result {i}:**\n```{chunk}```")
    # Concatenate all retrieved metadata for LLM context
    context = "\n".join(results)
    with st.spinner("Generating answer with LLM..."):
        answer = answer_question_with_context(user_query, context)
    st.subheader("LLM Answer:")
    st.markdown(f"> {answer}")

st.markdown("---")
st.markdown("Built with open-source RAG, FAISS, and Streamlit.")
