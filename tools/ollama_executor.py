import requests
import json

def run_ollama(model, prompt, endpoint):
    """
    Sends a prompt to an Ollama model running on a remote machine
    and returns the generated text response.
    Handles streaming output correctly.
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    response = requests.post(
        f"{endpoint}/api/generate",
        json=payload,
        stream=True,
        timeout=120
    )

    response.raise_for_status()

    full_text = ""

    # Ollama streams JSON objects line-by-line
    for line in response.iter_lines():
        if not line:
            continue

        try:
            chunk = json.loads(line.decode("utf-8"))
        except json.JSONDecodeError:
            # If Ollama ever emits raw text, append it safely
            full_text += line.decode("utf-8")
            continue

        # Append any text in the "response" field
        if "response" in chunk:
            full_text += chunk["response"]

        # Stop when Ollama signals completion
        if chunk.get("done"):
            break

    return full_text.strip()
