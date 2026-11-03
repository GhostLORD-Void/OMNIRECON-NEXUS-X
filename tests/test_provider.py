import pytest

from omnirecon.providers import HybridModelRouter, ProviderNotConfigured


def test_router_requires_at_least_one_configured_provider(monkeypatch):
    from omnirecon import providers
    monkeypatch.setattr(providers.settings, "provider_order", "openai,anthropic,google,local")
    monkeypatch.setattr(providers.settings, "openai_base_url", "")
    monkeypatch.setattr(providers.settings, "openai_api_key", "")
    monkeypatch.setattr(providers.settings, "openai_model", "")
    monkeypatch.setattr(providers.settings, "anthropic_api_key", "")
    monkeypatch.setattr(providers.settings, "google_api_key", "")
    monkeypatch.setattr(providers.settings, "local_model_base_url", "")
    assert HybridModelRouter().configured() == []


@pytest.mark.asyncio
async def test_router_raises_clear_error_without_provider():
    from omnirecon import providers
    monkeypatch_values = {
        "provider_order": "openai,anthropic,google,local",
        "openai_base_url": "", "openai_api_key": "", "openai_model": "",
        "anthropic_api_key": "", "google_api_key": "",
        "local_model_base_url": "", "local_model_name": "",
    }
    for key, value in monkeypatch_values.items():
        setattr(providers.settings, key, value)
    with pytest.raises(ProviderNotConfigured):
        await HybridModelRouter().complete("hello")


def test_provider_order_filters_unconfigured(monkeypatch):
    from omnirecon import providers
    monkeypatch.setattr(providers.settings, "provider_order", "local,openai,anthropic")
    monkeypatch.setattr(providers.settings, "local_model_base_url", "http://127.0.0.1:11434/v1")
    monkeypatch.setattr(providers.settings, "local_model_name", "llama3")
    monkeypatch.setattr(providers.settings, "openai_base_url", "")
    monkeypatch.setattr(providers.settings, "openai_api_key", "")
    monkeypatch.setattr(providers.settings, "openai_model", "")
    monkeypatch.setattr(providers.settings, "anthropic_api_key", "")
    assert HybridModelRouter().configured() == [("local", "llama3")]
