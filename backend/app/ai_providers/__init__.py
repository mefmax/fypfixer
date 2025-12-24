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


def get_ai_provider() -> 'AIProvider':
    """
    Factory function to get configured AI provider.

    Controlled by AI_PROVIDER environment variable:
    - 'local' or 'static': StaticProvider (default, no AI needed)
    - 'ollama': OllamaProvider (local AI)
    - 'anthropic': AnthropicProvider (production)

    Returns:
        Configured AI provider instance
    """
    provider_type = os.environ.get('AI_PROVIDER', 'static').lower()

    if provider_type in ('local', 'static'):
        from .static_provider import StaticProvider
        provider = StaticProvider()
        logger.info("Using Static provider (fallback)")
        return provider

    elif provider_type == 'ollama':
        from .ollama_provider import OllamaProvider
        provider = OllamaProvider()
        logger.info(f"Using Ollama provider: {provider.name}")
        return provider

    elif provider_type == 'anthropic':
        from .anthropic_provider import AnthropicProvider
        provider = AnthropicProvider()
        if provider.is_available():
            logger.info(f"Using Anthropic provider: {provider.name}")
            return provider
        else:
            logger.warning("Anthropic not configured, falling back to Static")
            from .static_provider import StaticProvider
            return StaticProvider()

    else:
        # Default to static for unknown values
        logger.warning(f"Unknown AI_PROVIDER '{provider_type}', using static")
        from .static_provider import StaticProvider
        return StaticProvider()


def get_provider_status() -> dict:
    """Get status of all available providers"""
    from .static_provider import StaticProvider
    from .ollama_provider import OllamaProvider
    from .anthropic_provider import AnthropicProvider

    static = StaticProvider()
    ollama = OllamaProvider()
    anthropic = AnthropicProvider()

    return {
        'static': {
            'available': static.is_available(),
            'name': 'Static Fallback'
        },
        'ollama': {
            'available': ollama.is_available(),
            'name': ollama.name
        },
        'anthropic': {
            'available': anthropic.is_available(),
            'name': anthropic.name
        },
        'current': os.environ.get('AI_PROVIDER', 'static')
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
