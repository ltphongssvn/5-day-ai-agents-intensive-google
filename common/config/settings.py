# common/config/settings.py - Configuration and environment variable management

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
        self.google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")

    def validate(self) -> bool:
        """Check if required API keys are present."""
        return bool(self.openai_api_key or self.anthropic_api_key or self.google_api_key)

    def get_available_providers(self) -> list[str]:
        """Return list of configured providers."""
        providers = []
        if self.openai_api_key:
            providers.append("openai")
        if self.anthropic_api_key:
            providers.append("anthropic")
        if self.google_api_key:
            providers.append("google")
        return providers


# Global settings instance
settings = Settings()