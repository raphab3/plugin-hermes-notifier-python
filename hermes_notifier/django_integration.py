"""
Django integration for Hermes Notifier
"""

import logging
from typing import Dict, List, Optional, Any
from django.conf import settings
try:
    from django.template.context_processors import RequestContext
except ImportError:
    # RequestContext was removed in newer Django versions
    RequestContext = None
from django.http import HttpRequest
from .client import HermesNotifier
from .exceptions import HermesNotifierError

logger = logging.getLogger(__name__)


class HermesNotificationMixin:
    """
    Mixin for Django views to easily send notifications
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hermes_client = None
    
    @property
    def hermes(self) -> HermesNotifier:
        """
        Get or create Hermes client instance
        """
        if self._hermes_client is None:
            base_url = getattr(settings, 'HERMES_BASE_URL', 'http://localhost:8000')
            token = getattr(settings, 'HERMES_TOKEN', None)
            
            if not token:
                raise HermesNotifierError(
                    "HERMES_TOKEN setting is required. "
                    "Please set it in your Django settings."
                )
            
            self._hermes_client = HermesNotifier(
                base_url=base_url,
                token=token,
                timeout=getattr(settings, 'HERMES_TIMEOUT', 30),
                verify_ssl=getattr(settings, 'HERMES_VERIFY_SSL', True)
            )
        
        return self._hermes_client
    
    def send_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        source_system: Optional[str] = None,
        priority: str = 'normal',
        channels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a notification to a user
        
        Args:
            user_id: ID of the user to notify
            title: Notification title
            body: Notification body
            source_system: System that generated the notification (default: Django app name)
            priority: Priority level ('low', 'normal', 'high', 'critical')
            channels: List of channels to send through
            metadata: Additional metadata dictionary
            
        Returns:
            Dictionary with notification details
        """
        if source_system is None:
            source_system = getattr(settings, 'HERMES_DEFAULT_SOURCE', 'django-app')
        
        try:
            return self.hermes.send_notification(
                user_id=user_id,
                title=title,
                body=body,
                source_system=source_system,
                priority=priority,
                channels=channels,
                metadata=metadata
            )
        except HermesNotifierError as e:
            logger.error(f"Failed to send notification: {e}")
            if getattr(settings, 'HERMES_RAISE_EXCEPTIONS', False):
                raise
            return {'success': False, 'error': str(e)}
    
    def send_group_notification(
        self,
        group_id: str,
        title: str,
        body: str,
        source_system: Optional[str] = None,
        priority: str = 'normal',
        channels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a notification to all members of a group
        
        Args:
            group_id: ID of the group to notify
            title: Notification title
            body: Notification body
            source_system: System that generated the notification
            priority: Priority level ('low', 'normal', 'high', 'critical')
            channels: List of channels to send through
            metadata: Additional metadata dictionary
            
        Returns:
            Dictionary with group notification results
        """
        if source_system is None:
            source_system = getattr(settings, 'HERMES_DEFAULT_SOURCE', 'django-app')
        
        try:
            return self.hermes.send_group_notification(
                group_id=group_id,
                title=title,
                body=body,
                source_system=source_system,
                priority=priority,
                channels=channels,
                metadata=metadata
            )
        except HermesNotifierError as e:
            logger.error(f"Failed to send group notification: {e}")
            if getattr(settings, 'HERMES_RAISE_EXCEPTIONS', False):
                raise
            return {'success': False, 'error': str(e)}
    
    def get_user_notifications(
        self,
        user_id: str,
        is_read: Optional[bool] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get notifications for a user
        
        Args:
            user_id: ID of the user
            is_read: Filter by read status (None for all)
            limit: Number of notifications to return
            
        Returns:
            List of notification dictionaries
        """
        try:
            response = self.hermes.get_notifications(
                user_id=user_id,
                is_read=is_read,
                limit=limit
            )
            return response.get('results', [])
        except HermesNotifierError as e:
            logger.error(f"Failed to get notifications: {e}")
            if getattr(settings, 'HERMES_RAISE_EXCEPTIONS', False):
                raise
            return []
    
    def get_unread_count(self, user_id: str) -> int:
        """
        Get count of unread notifications for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            Number of unread notifications
        """
        try:
            return self.hermes.get_unread_count(user_id)
        except HermesNotifierError as e:
            logger.error(f"Failed to get unread count: {e}")
            if getattr(settings, 'HERMES_RAISE_EXCEPTIONS', False):
                raise
            return 0


class HermesContextProcessor:
    """
    Django context processor to add Hermes notifications to template context
    """
    
    def __init__(self):
        self._hermes_client = None
    
    @property
    def hermes(self) -> HermesNotifier:
        """
        Get or create Hermes client instance
        """
        if self._hermes_client is None:
            base_url = getattr(settings, 'HERMES_BASE_URL', 'http://localhost:8000')
            token = getattr(settings, 'HERMES_TOKEN', None)
            
            if not token:
                logger.warning(
                    "HERMES_TOKEN setting is not configured. "
                    "Hermes notifications will not be available in templates."
                )
                return None
            
            self._hermes_client = HermesNotifier(
                base_url=base_url,
                token=token,
                timeout=getattr(settings, 'HERMES_TIMEOUT', 30),
                verify_ssl=getattr(settings, 'HERMES_VERIFY_SSL', True)
            )
        
        return self._hermes_client
    
    def __call__(self, request: HttpRequest) -> Dict[str, Any]:
        """
        Add Hermes notifications to template context
        
        Args:
            request: Django HTTP request
            
        Returns:
            Dictionary with Hermes context data
        """
        context = {
            'hermes_config': {
                'base_url': getattr(settings, 'HERMES_BASE_URL', 'http://localhost:8000'),
                'sse_enabled': getattr(settings, 'HERMES_SSE_ENABLED', True),
            },
            'hermes_notifications': [],
            'hermes_unread_count': 0,
        }
        
        # Only add notifications if user is authenticated and has a user ID
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return context
        
        # Get user ID from user model or settings
        user_id = self._get_user_id(request.user)
        if not user_id:
            return context
        
        # Add user ID to context
        context['hermes_user_id'] = user_id
        
        if self.hermes is None:
            return context
        
        try:
            # Get recent notifications for the user
            limit = getattr(settings, 'HERMES_CONTEXT_LIMIT', 10)
            notifications_data = self.hermes.get_notifications(
                user_id=user_id,
                limit=limit
            )
            
            context['hermes_notifications'] = notifications_data.get('results', [])
            
            # Get unread count
            context['hermes_unread_count'] = self.hermes.get_unread_count(user_id)
            
        except HermesNotifierError as e:
            logger.error(f"Failed to get notifications for context: {e}")
            # Don't raise exception in context processor
        
        return context
    
    def _get_user_id(self, user) -> Optional[str]:
        """
        Get user ID for Hermes notifications
        
        Args:
            user: Django user object
            
        Returns:
            User ID string or None
        """
        # Try different approaches to get user ID
        user_id_field = getattr(settings, 'HERMES_USER_ID_FIELD', None)
        
        if user_id_field:
            # Use custom field
            return str(getattr(user, user_id_field, None) or '')
        
        # Try common patterns
        if hasattr(user, 'external_user_id'):
            return user.external_user_id
        elif hasattr(user, 'profile') and hasattr(user.profile, 'external_user_id'):
            return user.profile.external_user_id
        elif hasattr(user, 'username'):
            return user.username
        else:
            return str(user.id)


# Convenience function for context processor
def hermes_notifications(request: HttpRequest) -> Dict[str, Any]:
    """
    Context processor function for Django templates
    
    Usage in settings.py:
    TEMPLATES = [
        {
            'OPTIONS': {
                'context_processors': [
                    'hermes_notifier.django_integration.hermes_notifications',
                ],
            },
        },
    ]
    """
    processor = HermesContextProcessor()
    return processor(request)


# Template tags module reference
def get_hermes_notifications_tags():
    """
    Get template tags for Hermes notifications
    
    Returns the module path for template tags
    """
    return 'hermes_notifier.templatetags.hermes_tags'