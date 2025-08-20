

import gradio as gr
import pandas as pd
import tempfile
import os
from rag_pipeline import build_faiss_index, search_metadata
from metadata_indexer import extract_metadata
from llm_answer import answer_question_with_context

metadata_chunks = []
faiss_built = False

def upload_files(files):
    global metadata_chunks, faiss_built
    metadata_chunks = []
    for uploaded_file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            tmp.write(uploaded_file)
            tmp_path = tmp.name
        meta = extract_metadata(tmp_path)
        metadata_chunks.append(meta)
        os.unlink(tmp_path)
    build_faiss_index(metadata_chunks)
    faiss_built = True
    return f"Indexed {len(files)} dataset(s)!"

def answer_question(user_query):
    if not faiss_built or not metadata_chunks:
        return "Please upload and index datasets first."
    results = search_metadata(user_query)
    context = "\n".join(results)
    answer = answer_question_with_context(user_query, context)
    return answer

with gr.Blocks() as demo:
    gr.Markdown("# Conversational Data Catalog with Advanced RAG (Gradio)")
    file_upload = gr.File(label="Upload CSV files", file_count="multiple", type="binary")
    upload_btn = gr.Button("Index Datasets")
    upload_output = gr.Textbox(label="Indexing Status")
    user_query = gr.Textbox(label="Ask a question about your data catalog")
    answer_output = gr.Textbox(label="LLM Answer")

    upload_btn.click(upload_files, inputs=[file_upload], outputs=[upload_output])
    user_query.submit(answer_question, inputs=[user_query], outputs=[answer_output])

    gr.Markdown("---\nBuilt with open-source RAG, FAISS, and Gradio.")

if __name__ == "__main__":
    demo.launch()
