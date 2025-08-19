



import os
from huggingface_hub import InferenceClient


def get_hf_token():
    # Prefer environment variable for cloud deployment
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("Hugging Face token not found in environment variable 'HF_TOKEN'. Please set it in your deployment secrets or environment.")
    return token

def answer_question_with_context(question, context, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
    """
    Use Meta-Llama-3-8B-Instruct via huggingface_hub InferenceClient and HF token.
    """
    hf_token = get_hf_token()
    os.environ["HF_TOKEN"] = hf_token
    client = InferenceClient(
        provider="novita",
        api_key=hf_token,
    )
    system_prompt = (
        "You are a helpful assistant for a data catalog. "
        "Given the following metadata about datasets, answer the user's question in detail. "
        "If the question asks for a statistical summary, explain each metric (mean, std, min, max, nulls, etc.) in simple terms. "
        "If the answer is not present, say so honestly."
    )
    user_prompt = (
        f"Metadata:\n{context}\n"
        f"Question: {question}\nAnswer:"
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content.strip() if hasattr(completion.choices[0].message, 'content') else str(completion.choices[0].message)
