import os


# Ensure required environment variables exist during test collection/import.
os.environ.setdefault("ENV_MODE", "test")
os.environ.setdefault("OPENROUTER_API_KEY", "dummy-test-key")
os.environ.setdefault("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
os.environ.setdefault("OPENROUTER_MODEL", "openai/gpt-4o-mini")
