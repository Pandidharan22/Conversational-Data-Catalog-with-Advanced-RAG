


import gradio as gr
import pandas as pd
import tempfile
import os
from rag_pipeline import build_faiss_index, search_metadata
from metadata_indexer import extract_metadata
from llm_answer import answer_question_with_context

metadata_chunks = []
faiss_built = False

def upload_and_index(files):
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
    return "Indexing complete. You can now ask questions about your data!", gr.update(visible=True), []

def chat_qa(history, user_query):
    if history is None:
        history = []
    if not faiss_built or not metadata_chunks:
        history.append({"role": "user", "content": user_query})
        history.append({"role": "assistant", "content": "Please upload and index datasets first."})
        return history, ""
    history.append({"role": "user", "content": user_query})
    results = search_metadata(user_query)
    context = "\n".join(results)
    answer = answer_question_with_context(user_query, context)
    history.append({"role": "assistant", "content": answer})
    return history, ""

with gr.Blocks() as demo:
    gr.Markdown("# Conversational Data Catalog with Advanced RAG")
    with gr.Row():
        with gr.Column():
            file_upload = gr.File(label="Upload CSV files", file_count="multiple", type="binary")
            status_text = gr.Markdown("", visible=False)
        with gr.Column():
            chatbot = gr.Chatbot(label="Chat about your data catalog", visible=False, type="messages")
            user_input = gr.Textbox(label="Ask a question", visible=False)

    def on_upload(files):
        # Show "Analysing the Dataset" while indexing
        analysing = gr.update(value="Analysing the Dataset", visible=True)
        yield analysing, gr.update(visible=False), gr.update(visible=False)
        # Do the indexing
        indexing_status, _, _ = upload_and_index(files)
        # After indexing, show chat and input (history as empty list)
        yield gr.update(value=indexing_status, visible=True), gr.update(visible=True, value=[]), gr.update(visible=True)

    file_upload.upload(
        fn=on_upload,
        inputs=[file_upload],
        outputs=[status_text, chatbot, user_input],
        queue=True
    )

    user_input.submit(
        fn=chat_qa,
        inputs=[chatbot, user_input],
        outputs=[chatbot, user_input]
    )

    gr.Markdown("---\nBuilt with open-source RAG, FAISS, and Gradio.")

if __name__ == "__main__":
    demo.launch()
