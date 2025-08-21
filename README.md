
# Conversational Data Catalog with Advanced RAG

## Overview

This project is a conversational chatbot app that allows you to upload CSV datasets, automatically indexes them, and answers your questions using Retrieval-Augmented Generation (RAG) and open-source LLMs. The app is built with Gradio for the UI and is designed for both local and cloud (Hugging Face Spaces) deployment.

**Try the app live:** [Conversational Data Catalogue on Hugging Face Spaces](https://huggingface.co/spaces/Pandidharan22/Conversational_Data_Catalogue)

## Features

- **Automatic Dataset Indexing:** Upload CSV files and they are instantly indexed for search.
- **Conversational Chatbot:** Ask questions about your data and see the full conversation history.
- **Open-Source RAG:** Uses FAISS for vector search and open LLMs for answers.
- **Secure:** No secrets or tokens are stored in the repo. Uses `.env` for local development.

## Architecture

This project is designed with a modular, production-grade architecture:

- **Frontend/UI:** Built with [Gradio](https://gradio.app/) (v5.x), providing a modern, responsive web interface for file upload and conversational chat.
- **Metadata Extraction:** Each uploaded CSV is processed by `metadata_indexer.py` to extract schema, column types, and sample data using [pandas](https://pandas.pydata.org/) (v2.x).
- **Vector Store (RAG):** Extracted metadata is embedded using [sentence-transformers](https://www.sbert.net/) (v5.x) and indexed with [FAISS](https://github.com/facebookresearch/faiss) (v1.12+) for efficient similarity search (`rag_pipeline.py`).
- **LLM Integration:** User questions are answered by retrieving relevant metadata chunks and passing them, along with the question, to an open-source LLM (e.g., Meta-Llama-3-8B-Instruct) via [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) (v4.55+) and the Hugging Face Inference API (`llm_answer.py`).
- **Secrets Management:** Sensitive tokens (e.g., `HF_TOKEN`) are loaded from a `.env` file (local, via [python-dotenv](https://pypi.org/project/python-dotenv/)) or Hugging Face Space secrets (cloud).

## Tech Stack & Dependencies

- **Python:** 3.10+
- **Gradio:** v5.43.1 — UI framework
- **pandas:** v2.3.1 — Data manipulation and CSV parsing
- **sentence-transformers:** v5.1.0 — Embedding generation
- **transformers:** v4.55.3 — LLM inference and embeddings
- **faiss-cpu:** v1.12.0 — Vector similarity search
- **python-dotenv:** v1.1.1 — Local secret management
- **langchain:** v0.3.27 — (Optional) for advanced RAG workflows
- **chromadb:** v1.0.20 — (Optional) for alternative vector DB support
- **llama-cpp-python:** v0.3.16 — *Only required for local Llama.cpp inference. Not needed for web/cloud deployment (Hugging Face Spaces uses hosted models).* 
- **Hugging Face Spaces** — For cloud deployment
- **GitHub Copilot** — Used for code suggestions and productivity

**Note:** For web/cloud deployment (Hugging Face Spaces), you do **not** need `llama-cpp-python`. It is only required for local CPU-based Llama.cpp inference. For Spaces, all LLM inference is handled via the Hugging Face Inference API and hosted models.

### Main Models Used
- **Meta-Llama-3-8B-Instruct** (via Hugging Face Inference API)
- *You can swap in any open-source LLM available on Hugging Face Hub by changing the model name in `llm_answer.py`.*

## Workflow

1. **User uploads CSV files** via the Gradio interface.
2. **App extracts metadata** (columns, types, samples) from each file using pandas.
3. **Metadata is embedded** using sentence-transformers and indexed in FAISS for fast retrieval.
4. **User asks a question** in the chat interface.
5. **Relevant metadata is retrieved** from FAISS based on the question.
6. **LLM receives the question and context** and generates a natural language answer using the selected model.
7. **Conversation history** is displayed, allowing follow-up questions.

## How to Use

1. **Upload** one or more CSV files.
2. Wait for the “Analysing the Dataset” message.
3. Once indexing is complete, ask questions in the chat interface.
4. Continue the conversation as needed!

## Local Setup

1. Clone the repository:
	```bash
	git clone https://github.com/Pandidharan22/Conversational-Data-Catalog-with-Advanced-RAG.git
	cd Conversational-Data-Catalog-with-Advanced-RAG
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Add your Hugging Face token to a `.env` file (if required for LLM access):
	```env
	HF_TOKEN=your_huggingface_token
	```
4. Run the app:
	```bash
	python app.py
	# or for a public link
	python app.py --share
	```

## Cloud Deployment (Hugging Face Spaces)

1. Create a new Space at https://huggingface.co/spaces (choose Gradio SDK).
2. Link your GitHub repo or upload your files.
3. Add any required secrets (like `HF_TOKEN`) in the Space settings.
4. Your app will be live and public!

## File Structure

- `app.py` — Main Gradio app
- `rag_pipeline.py` — RAG and FAISS logic
- `metadata_indexer.py` — Metadata extraction
- `llm_answer.py` — LLM answer logic
- `requirements.txt` — Python dependencies
- `data/` — Example datasets
- `.env` — Local secrets (not tracked by git)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Built with Gradio, FAISS, Hugging Face Transformers, and open-source LLMs.*