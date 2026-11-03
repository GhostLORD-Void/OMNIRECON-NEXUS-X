import pytest
from omnirecon.providers import OpenAICompatibleProvider, ProviderNotConfigured

def test_provider_requires_credentials():
    with pytest.raises(ProviderNotConfigured):
        OpenAICompatibleProvider(base_url="", api_key="", model="")

def test_provider_rejects_insecure_remote_endpoint():
    with pytest.raises(ValueError):
        OpenAICompatibleProvider(base_url="http://example.com/v1", api_key="secret", model="model")
