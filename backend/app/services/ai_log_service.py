"""
AI Request Logging Service - tracks AI usage, cost, and latency.

Usage:
    from app.services.ai_log_service import ai_log_service

    ai_log_service.log_request(
        user_id=1,
        provider='anthropic',
        model='claude-3-haiku-20240307',
        latency_ms=1200,
        prompt_tokens=100,
        completion_tokens=500
    )
"""

import logging
from typing import Optional
from decimal import Decimal

from app import db
from app.models import AIRequestLog

logger = logging.getLogger(__name__)


class AILogService:
    """Service for logging AI API requests and calculating costs."""

    # Pricing per 1M tokens (USD)
    PRICING = {
        'claude-3-haiku-20240307': {
            'input': Decimal('0.25'),
            'output': Decimal('1.25')
        },
        'claude-3-5-haiku-20241022': {
            'input': Decimal('1.00'),
            'output': Decimal('5.00')
        },
        'claude-3-5-sonnet-20241022': {
            'input': Decimal('3.00'),
            'output': Decimal('15.00')
        },
        'static': {
            'input': Decimal('0'),
            'output': Decimal('0')
        },
        'ollama': {
            'input': Decimal('0'),
            'output': Decimal('0')
        }
    }

    def calculate_cost(
        self,
        model: str,
        prompt_tokens: Optional[int],
        completion_tokens: Optional[int]
    ) -> Optional[Decimal]:
        """
        Calculate cost in USD based on token usage and model pricing.

        Args:
            model: Model identifier
            prompt_tokens: Number of input tokens
            completion_tokens: Number of output tokens

        Returns:
            Cost in USD or None if cannot calculate
        """
        if not prompt_tokens and not completion_tokens:
            return None

        pricing = self.PRICING.get(model)
        if not pricing:
            # Unknown model - try to find partial match
            for known_model, known_pricing in self.PRICING.items():
                if known_model in model or model in known_model:
                    pricing = known_pricing
                    break

        if not pricing:
            logger.warning(f"Unknown model for pricing: {model}")
            return None

        cost = Decimal('0')

        if prompt_tokens:
            cost += (Decimal(prompt_tokens) / Decimal('1000000')) * pricing['input']

        if completion_tokens:
            cost += (Decimal(completion_tokens) / Decimal('1000000')) * pricing['output']

        return cost

    def log_request(
        self,
        provider: str,
        model: str,
        latency_ms: int,
        user_id: Optional[int] = None,
        prompt_tokens: Optional[int] = None,
        completion_tokens: Optional[int] = None,
        error: Optional[str] = None
    ) -> AIRequestLog:
        """
        Log an AI API request to the database.

        Args:
            provider: Provider name ('anthropic', 'static', 'ollama')
            model: Model identifier
            latency_ms: Request latency in milliseconds
            user_id: Optional user ID
            prompt_tokens: Optional input token count
            completion_tokens: Optional output token count
            error: Optional error message if request failed

        Returns:
            Created AIRequestLog instance
        """
        # Calculate cost
        cost_usd = self.calculate_cost(model, prompt_tokens, completion_tokens)

        # Create log entry
        log_entry = AIRequestLog(
            user_id=user_id,
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            error=error
        )

        try:
            db.session.add(log_entry)
            db.session.commit()

            if error:
                logger.info(
                    f"AI request logged: provider={provider}, model={model}, "
                    f"latency={latency_ms}ms, error={error[:50]}..."
                )
            else:
                logger.info(
                    f"AI request logged: provider={provider}, model={model}, "
                    f"latency={latency_ms}ms, tokens={prompt_tokens}/{completion_tokens}, "
                    f"cost=${cost_usd:.6f}" if cost_usd else f"cost=N/A"
                )

        except Exception as e:
            logger.error(f"Failed to log AI request: {e}")
            db.session.rollback()

        return log_entry


# Singleton instance
ai_log_service = AILogService()
