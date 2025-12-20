"""
AI Provider abstraction for FYPFixer recommendation engine.

Usage:
    from app.ai_providers import get_ai_provider

    provider = get_ai_provider()
    criteria = provider.generate_criteria(user_context)
    actions = provider.select_actions(candidates, user_context)
"""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import AIProvider


def get_ai_provider() -> 'AIProvider':
    """
    Factory function to get configured AI provider.

    Controlled by AI_PROVIDER environment variable:
    - 'local' or 'ollama': OllamaProvider (default, free)
    - 'openai': OpenAIProvider ($1-15/mo)
    - 'anthropic': AnthropicProvider ($3-10/mo)

    Returns:
        Configured AIProvider instance
    """
    provider_type = os.environ.get('AI_PROVIDER', 'local').lower()

    if provider_type in ('local', 'ollama'):
        from .local_provider import LocalProvider
        return LocalProvider()

    elif provider_type == 'openai':
        from .openai_provider import OpenAIProvider
        return OpenAIProvider()

    elif provider_type == 'anthropic':
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider()

    else:
        # Default to local for unknown values
        print(f"Warning: Unknown AI_PROVIDER '{provider_type}', using local")
        from .local_provider import LocalProvider
        return LocalProvider()


# Re-export base class for type hints
from .base import AIProvider

__all__ = ['AIProvider', 'get_ai_provider']
