"""
AI Provider abstraction for FYPGlow recommendation engine.

Usage:
    from app.ai_providers import get_ai_provider

    provider = get_ai_provider()
    plan = provider.generate_plan(categories, display_name, streak)
"""

import os
import logging
from typing import Union

logger = logging.getLogger(__name__)


def get_ai_provider() -> Union['OllamaProvider', 'AnthropicProvider']:
    """
    Factory function to get configured AI provider.

    Controlled by AI_PROVIDER environment variable:
    - 'local' or 'ollama': OllamaProvider (default, free)
    - 'anthropic': AnthropicProvider (production)

    Returns:
        Configured AI provider instance
    """
    provider_type = os.environ.get('AI_PROVIDER', 'ollama').lower()

    if provider_type == 'anthropic':
        from .anthropic_provider import AnthropicProvider
        provider = AnthropicProvider()
        if provider.is_available():
            logger.info(f"Using Anthropic provider: {provider.name}")
            return provider
        else:
            logger.warning("Anthropic not configured, falling back to Ollama")
            provider_type = 'ollama'

    # Default: Ollama (local)
    from .ollama_provider import OllamaProvider
    provider = OllamaProvider()
    logger.info(f"Using Ollama provider: {provider.name}")
    return provider


def get_provider_status() -> dict:
    """Get status of all available providers"""
    from .ollama_provider import OllamaProvider
    from .anthropic_provider import AnthropicProvider

    ollama = OllamaProvider()
    anthropic = AnthropicProvider()

    return {
        'ollama': {
            'available': ollama.is_available(),
            'name': ollama.name
        },
        'anthropic': {
            'available': anthropic.is_available(),
            'name': anthropic.name
        },
        'current': os.environ.get('AI_PROVIDER', 'ollama')
    }


# Keep old imports for backward compatibility
from .base import AIProvider, UserContext, SearchCriteria, SelectedAction
from .local_provider import LocalProvider

__all__ = [
    'get_ai_provider',
    'get_provider_status',
    # Legacy exports
    'AIProvider',
    'UserContext',
    'SearchCriteria',
    'SelectedAction',
    'LocalProvider',
]
