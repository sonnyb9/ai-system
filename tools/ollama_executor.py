import requests
import json
from tools.logger import log

def run_ollama(model, prompt, endpoint):
    """
    Sends a prompt to an Ollama model running on a remote machine
    and returns the generated text response.
    """

    payload = {
        "model": model,
        "prompt": prompt
    }

    try:
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

        # Unexpected response format
        log(f"Unexpected Ollama response format for model {model}: {type(data)}")
        return ""

    except requests.RequestException as e:
        log(f"Ollama request failed for model {model}: {e}")
        return ""
    except json.JSONDecodeError as e:
        log(f"Failed to parse Ollama response for model {model}: {e}")
        return ""

