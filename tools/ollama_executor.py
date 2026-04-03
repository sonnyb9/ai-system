import requests
import json

def run_ollama(model, prompt, endpoint):
    """
    Sends a prompt to an Ollama model running on a remote machine
    and returns the generated text response.
    """

    payload = {
        "model": model,
        "prompt": prompt
    }

    response = requests.post(
        f"{endpoint}/api/generate",
        json=payload,
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    # Ollama returns streaming chunks unless "stream": false is set.
    # If your model returns chunks, concatenate them here.
    if isinstance(data, dict) and "response" in data:
        return data["response"]

    # If streaming mode is enabled, Ollama returns a list of chunks.
    if isinstance(data, list):
        return "".join(chunk.get("response", "") for chunk in data)

    return ""

