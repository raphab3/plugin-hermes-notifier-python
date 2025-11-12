"""
Custom exceptions for Hermes Notifier
"""


class HermesNotifierError(Exception):
    """Base exception for Hermes Notifier"""
    pass


class AuthenticationError(HermesNotifierError):
    """Raised when authentication fails"""
    pass


class ConnectionError(HermesNotifierError):
    """Raised when connection to Hermes API fails"""
    pass


class ValidationError(HermesNotifierError):
    """Raised when request validation fails"""
    pass


class RateLimitError(HermesNotifierError):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after