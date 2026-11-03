"""Multi-provider model gateway with deterministic fallback.

All providers are opt-in through environment configuration. No credentials are
returned by the API. The local provider uses an OpenAI-compatible endpoint.
"""
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

import httpx

from omnirecon.config import settings


class ProviderNotConfigured(RuntimeError):
    pass


@dataclass(frozen=True)
class ProviderResult:
    provider: str
    model: str
    text: str


class HybridModelRouter:
    def __init__(self, timeout: float | None = None):
        self.timeout = timeout or settings.model_timeout_seconds

    def configured(self) -> list[tuple[str, str]]:
        available = {
            "openai": bool(settings.openai_base_url and settings.openai_api_key and settings.openai_model),
            "anthropic": bool(settings.anthropic_api_key and settings.anthropic_model),
            "google": bool(settings.google_api_key and settings.google_model),
            "local": bool(settings.local_model_base_url and settings.local_model_name),
        }
        order = [item.strip().lower() for item in settings.provider_order.split(",") if item.strip()]
        return [(name, self._model(name)) for name in order if available.get(name, False)]

    def _model(self, name: str) -> str:
        return {
            "openai": settings.openai_model,
            "anthropic": settings.anthropic_model,
            "google": settings.google_model,
            "local": settings.local_model_name,
        }[name]

    async def complete(self, prompt: str) -> ProviderResult:
        providers = self.configured()
        if not providers:
            raise ProviderNotConfigured(
                "No model provider configured. Add provider credentials to your local .env."
            )
        errors: list[str] = []
        for name, model in providers:
            try:
                text = await self._request(name, model, prompt)
                return ProviderResult(provider=name, model=model, text=text)
            except (httpx.HTTPError, RuntimeError, ValueError) as exc:
                errors.append(f"{name}: {type(exc).__name__}")
        raise RuntimeError("All configured model providers failed: " + "; ".join(errors))

    async def _request(self, name: str, model: str, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if name in ("openai", "local"):
                base = settings.openai_base_url if name == "openai" else settings.local_model_base_url
                key = settings.openai_api_key if name == "openai" else settings.local_model_api_key
                parsed = urlparse(base)
                local_hosts = {"localhost", "127.0.0.1", "::1"}
                if parsed.scheme != "https" and not (
                    parsed.scheme == "http" and parsed.hostname in local_hosts
                ):
                    raise ValueError("Provider endpoint must use HTTPS, except exact localhost hosts")
                response = await client.post(
                    base.rstrip("/") + "/chat/completions",
                    headers={"Authorization": f"Bearer {key}"},
                    json={"model": model, "messages": [{"role": "user", "content": prompt}],
                          "temperature": 0.2},
                )
                response.raise_for_status()
                data: dict[str, Any] = response.json()
                try:
                    return str(data["choices"][0]["message"]["content"])
                except (KeyError, IndexError, TypeError) as exc:
                    raise RuntimeError("Invalid OpenAI-compatible response") from exc

            if name == "anthropic":
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"x-api-key": settings.anthropic_api_key,
                             "anthropic-version": "2023-06-01",
                             "content-type": "application/json"},
                    json={"model": model, "max_tokens": 1800,
                          "messages": [{"role": "user", "content": prompt}]},
                )
                response.raise_for_status()
                data = response.json()
                try:
                    return "\\n".join(
                        str(block["text"]) for block in data["content"] if block.get("type") == "text"
                    )
                except (KeyError, TypeError) as exc:
                    raise RuntimeError("Invalid Anthropic response") from exc

            if name == "google":
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                    headers={"x-goog-api-key": settings.google_api_key},
                    json={"contents": [{"parts": [{"text": prompt}]}],
                          "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1800}},
                )
                response.raise_for_status()
                data = response.json()
                try:
                    return "\\n".join(
                        str(part["text"])
                        for candidate in data["candidates"]
                        for part in candidate["content"]["parts"]
                        if "text" in part
                    )
                except (KeyError, TypeError) as exc:
                    raise RuntimeError("Invalid Gemini response") from exc

        raise ValueError(f"Unsupported provider: {name}")
