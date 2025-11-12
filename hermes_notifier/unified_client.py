"""
Unified Hermes client combining HTTP API and SSE in a single interface
"""

import logging
from typing import Callable, Optional, Dict, Any, List
from .client import HermesNotifier
from .sse_client import SSEClient
from .exceptions import HermesNotifierError

logger = logging.getLogger(__name__)


class HermesUnifiedClient:
    """
    Unified client that combines HTTP API and SSE functionality
    
    This is the recommended client for most use cases as it provides
    both API methods and real-time notifications in a single interface.
    
    Example:
        >>> from hermes_notifier import HermesUnifiedClient
        >>> 
        >>> def on_notification(notification):
        ...     print(f"New notification: {notification['title']}")
        >>> 
        >>> client = HermesUnifiedClient(
        ...     base_url='http://localhost:8000',
        ...     app_token='your-app-token',
        ...     profile_token='your-profile-token',  # Optional, for SSE
        ...     on_notification=on_notification
        ... )
        >>> 
        >>> # Send notification
        >>> client.send_notification(
        ...     user_id='user-123',
        ...     title='Hello',
        ...     body='Test message'
        ... )
        >>> 
        >>> # Get notifications
        >>> notifications = client.get_notifications('user-123')
        >>> 
        >>> # Mark as read
        >>> client.mark_as_read(notification_id)
        >>> 
        >>> # Start SSE (if profile_token provided)
        >>> client.start_sse()
        >>> 
        >>> # Stop SSE
        >>> client.stop_sse()
    """
    
    def __init__(
        self,
        base_url: str,
        app_token: str,
        profile_token: Optional[str] = None,
        on_notification: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_connect: Optional[Callable[[], None]] = None,
        on_disconnect: Optional[Callable[[], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        auto_start_sse: bool = False,
        timeout: int = 30,
        verify_ssl: bool = True,
        **sse_kwargs
    ):
        """
        Initialize unified client
        
        Args:
            base_url: Base URL of Hermes API
            app_token: Application token for API calls
            profile_token: Profile token for SSE (optional)
            on_notification: Callback when notification is received via SSE
            on_connect: Callback when SSE connects
            on_disconnect: Callback when SSE disconnects
            on_error: Callback when error occurs
            auto_start_sse: Automatically start SSE if profile_token provided
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            **sse_kwargs: Additional arguments for SSEClient
        """
        # Initialize HTTP client
        self.http_client = HermesNotifier(
            base_url=base_url,
            token=app_token,
            timeout=timeout,
            verify_ssl=verify_ssl
        )
        
        # Initialize SSE client if profile_token provided
        self.sse_client: Optional[SSEClient] = None
        if profile_token:
            self.sse_client = SSEClient(
                base_url=base_url,
                profile_token=profile_token,
                on_notification=on_notification,
                on_connect=on_connect,
                on_disconnect=on_disconnect,
                on_error=on_error,
                timeout=timeout,
                verify_ssl=verify_ssl,
                **sse_kwargs
            )
            
            if auto_start_sse:
                self.start_sse()
    
    # ========== Notification Methods ==========
    
    def send_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        source_system: str = 'python-client',
        priority: str = 'normal',
        channels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a notification to a user"""
        return self.http_client.send_notification(
            user_id=user_id,
            title=title,
            body=body,
            source_system=source_system,
            priority=priority,
            channels=channels,
            metadata=metadata
        )
    
    def send_group_notification(
        self,
        group_id: str,
        title: str,
        body: str,
        source_system: str = 'python-client',
        priority: str = 'normal',
        channels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a notification to all members of a group"""
        return self.http_client.send_group_notification(
            group_id=group_id,
            title=title,
            body=body,
            source_system=source_system,
            priority=priority,
            channels=channels,
            metadata=metadata
        )
    
    def get_notifications(
        self,
        user_id: str,
        is_read: Optional[bool] = None,
        priority: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get notifications for a user"""
        return self.http_client.get_notifications(
            user_id=user_id,
            is_read=is_read,
            priority=priority,
            limit=limit,
            offset=offset
        )
    
    def mark_as_read(self, notification_id: str) -> Dict[str, Any]:
        """Mark a notification as read"""
        return self.http_client.mark_as_read(notification_id)
    
    def mark_all_as_read(self, user_id: str) -> Dict[str, Any]:
        """Mark all notifications as read for a user"""
        return self.http_client.mark_all_as_read(user_id)
    
    def delete_notification(self, notification_id: str) -> Dict[str, Any]:
        """Delete a notification"""
        return self.http_client.delete_notification(notification_id)
    
    def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications for a user"""
        return self.http_client.get_unread_count(user_id)
    
    # ========== Group Methods ==========
    
    def create_group(
        self,
        name: str,
        description: str = '',
        member_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a notification group"""
        return self.http_client.create_group(
            name=name,
            description=description,
            member_ids=member_ids
        )
    
    # ========== Push Notification Methods ==========
    
    def register_device_token(
        self,
        user_id: str,
        device_token: str,
        platform: str = 'unknown'
    ) -> Dict[str, Any]:
        """Register a device token for push notifications"""
        return self.http_client.register_device_token(
            user_id=user_id,
            device_token=device_token,
            platform=platform
        )
    
    def unregister_device_token(
        self,
        user_id: str,
        device_token: str
    ) -> Dict[str, Any]:
        """Unregister a device token"""
        return self.http_client.unregister_device_token(
            user_id=user_id,
            device_token=device_token
        )
    
    # ========== SSE Methods ==========
    
    def start_sse(self):
        """Start SSE client in background"""
        if not self.sse_client:
            raise HermesNotifierError(
                "SSE client not initialized. Provide profile_token in constructor."
            )
        self.sse_client.start()
        logger.info("SSE client started")
    
    def stop_sse(self):
        """Stop SSE client"""
        if self.sse_client:
            self.sse_client.stop()
            logger.info("SSE client stopped")
    
    def is_sse_connected(self) -> bool:
        """Check if SSE is connected"""
        if not self.sse_client:
            return False
        return self.sse_client.is_connected()
    
    # ========== Utility Methods ==========
    
    def validate_token(self) -> bool:
        """Validate the current authentication token"""
        return self.http_client.validate_token()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup SSE"""
        self.stop_sse()
    
    def __repr__(self):
        sse_status = "connected" if self.is_sse_connected() else "disconnected"
        return f"HermesUnifiedClient(base_url='{self.http_client.base_url}', sse={sse_status})"

