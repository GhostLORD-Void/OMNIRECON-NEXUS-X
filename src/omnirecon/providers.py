"""OpenAI-compatible chat provider. No provider is contacted unless configured."""
from typing import Any
import httpx

class ProviderNotConfigured(RuntimeError):
    pass

class OpenAICompatibleProvider:
    def __init__(self, *, base_url: str, api_key: str, model: str, timeout: float = 45.0):
        if not base_url or not api_key or not model:
            raise ProviderNotConfigured("Set MODEL_BASE_URL, MODEL_API_KEY, and MODEL_NAME")
        if not base_url.startswith(("https://", "http://localhost", "http://127.0.0.1")):
            raise ValueError("Model endpoint must use HTTPS (HTTP is allowed only for localhost)")
        self.base_url, self.api_key, self.model, self.timeout = base_url.rstrip("/"), api_key, model, timeout

    async def complete(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2},
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        try:
            return str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Provider returned an unexpected chat-completions response") from exc
