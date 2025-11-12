"""
Hermes Notifier - Python/Django Plugin

A Python library for integrating Hermes notifications into Django applications.
"""

__version__ = "1.1.0"
__author__ = "Hermes Team"
__email__ = "team@hermes.dev"

from .client import HermesNotifier
from .unified_client import HermesUnifiedClient
from .sse_client import SSEClient, SSENotificationListener
from .django_integration import HermesNotificationMixin, HermesContextProcessor
from .exceptions import (
    HermesNotifierError,
    AuthenticationError,
    ConnectionError,
    ValidationError,
    RateLimitError
)

__all__ = [
    # Main clients
    "HermesNotifier",
    "HermesUnifiedClient",
    "SSEClient",
    "SSENotificationListener",

    # Django integration
    "HermesNotificationMixin",
    "HermesContextProcessor",

    # Exceptions
    "HermesNotifierError",
    "AuthenticationError",
    "ConnectionError",
    "ValidationError",
    "RateLimitError",
]