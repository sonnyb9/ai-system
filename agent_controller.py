import json
from tools.logger import log
from tools.ollama_executor import run_ollama

class AgentController:
    def __init__(self, config_root):
        self.config_root = config_root
        self.providers = self.load_providers()
        self.routing = self.load_routing()

    def load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def load_providers(self):
        providers_dir = f"{self.config_root}/providers"
        provider_files = ["aurora_local_deepseek.json"]  # expand later if needed

        providers = {}
        for file in provider_files:
            data = self.load_json(f"{providers_dir}/{file}")
            providers[data["provider_name"]] = data
        return providers

    def load_routing(self):
        return self.load_json(f"{self.config_root}/routing/routing.json")

    def run_task(self, task):
        prompt = task.get("prompt", "")
        if not prompt:
            log("Task missing prompt")
            return None

        for provider_name in self.routing["priority_order"]:
            provider = self.providers.get(provider_name)
            if not provider:
                continue

            try:
                log(f"Trying provider: {provider_name}")
                result = self.call_provider(provider, prompt)
                if result:
                    log(f"Provider {provider_name} succeeded")
                    return result
            except Exception as e:
                log(f"Provider {provider_name} failed: {e}")

        log("All providers failed")
        return None

    def call_provider(self, provider, prompt):
        if provider["type"] == "ollama":
            return run_ollama(
                model=provider["model"],
                prompt=prompt,
                endpoint=provider["endpoint"]
            )
        else:
            raise ValueError(f"Unknown provider type: {provider['type']}")

