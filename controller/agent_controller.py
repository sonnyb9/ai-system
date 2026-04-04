import json
from pathlib import Path
from tools.logger import log
from tools.ollama_executor import run_ollama

class AgentController:
    def __init__(self, config_root):
        self.config_root = Path(config_root)
        self.providers = self.load_providers()
        self.routing = self.load_routing()

    def load_json(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log(f"Error loading JSON from {path}: {e}")
            return {}

    def load_providers(self):
        providers_dir = self.config_root / "providers"
        providers = {}

        for file_path in providers_dir.glob("*.json"):
            try:
                data = self.load_json(file_path)
                if "provider_name" in data:
                    providers[data["provider_name"]] = data
                else:
                    log(f"Provider file {file_path.name} missing 'provider_name'")
            except Exception as e:
                log(f"Failed to load provider {file_path.name}: {e}")

        return providers

    def load_routing(self):
        routing_file = self.config_root / "routing" / "routing.json"
        return self.load_json(routing_file)

    def run_task(self, task):
        prompt = task.get("prompt", "")
        if not prompt:
            log("Task missing prompt")
            return {
                "success": False,
                "result": "",
                "error_code": "MISSING_PROMPT",
                "retriable": False
            }

        for provider_name in self.routing.get("priority_order", []):
            provider = self.providers.get(provider_name)
            if not provider:
                log(f"Provider {provider_name} not found")
                continue

            try:
                log(f"Trying provider: {provider_name}")
                result = self.call_provider(provider, prompt)
                if result:
                    log(f"Provider {provider_name} succeeded")
                    return {
                        "success": True,
                        "result": result,
                        "error_code": "",
                        "retriable": False
                    }
            except Exception as e:
                log(f"Provider {provider_name} failed: {e}")

        log("All providers failed")
        return {
            "success": False,
            "result": "",
            "error_code": "ALL_PROVIDERS_FAILED",
            "retriable": True
        }

    def call_provider(self, provider, prompt):
        if provider["type"] == "ollama":
            return run_ollama(
                model=provider["model"],
                prompt=prompt,
                endpoint=provider["endpoint"]
            )
        else:
            raise ValueError(f"Unknown provider type: {provider['type']}")

