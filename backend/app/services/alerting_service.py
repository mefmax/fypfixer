"""
Alerting Service - Send alerts to Telegram for system monitoring.

Alerts:
- critical: 🚨 Immediate action required
- warning: ⚠️ Attention needed
- info: ℹ️ Informational
"""

import os
import logging
import httpx

logger = logging.getLogger(__name__)


class AlertingService:
    """Service for sending alerts to Telegram."""

    def __init__(self):
        self.bot_token = os.getenv('ALERT_TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('ALERT_TELEGRAM_CHAT_ID')
        self.enabled = bool(self.bot_token and self.chat_id)

    def send_alert(self, severity: str, title: str, message: str) -> bool:
        """
        Send an alert to Telegram.

        Args:
            severity: 'critical', 'warning', or 'info'
            title: Alert title
            message: Alert body

        Returns:
            True if sent successfully, False otherwise
        """
        emoji = {
            'critical': '🚨',
            'warning': '⚠️',
            'info': 'ℹ️'
        }

        text = f"{emoji.get(severity, '📢')} *{title}*\n\n{message}"

        if not self.enabled:
            logger.warning(f"Alert (Telegram disabled): {severity} - {title}")
            print(f"[ALERT] {severity.upper()}: {title}\n{message}")
            return False

        try:
            response = httpx.post(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                json={
                    'chat_id': self.chat_id,
                    'text': text,
                    'parse_mode': 'Markdown'
                },
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Alert sent: {severity} - {title}")
            return True

        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return False

    def send_critical(self, title: str, message: str) -> bool:
        """Send a critical alert."""
        return self.send_alert('critical', title, message)

    def send_warning(self, title: str, message: str) -> bool:
        """Send a warning alert."""
        return self.send_alert('warning', title, message)

    def send_info(self, title: str, message: str) -> bool:
        """Send an info alert."""
        return self.send_alert('info', title, message)


# Singleton instance
alerting_service = AlertingService()
