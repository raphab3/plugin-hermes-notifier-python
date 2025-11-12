"""
SSE (Server-Sent Events) client for real-time notifications
"""

import json
import logging
import threading
import time
from typing import Callable, Optional, Dict, Any
import requests
from .exceptions import HermesNotifierError, AuthenticationError, ConnectionError

logger = logging.getLogger(__name__)


class SSEClient:
    """
    SSE client for receiving real-time notifications from Hermes
    
    Example:
        >>> from hermes_notifier import SSEClient
        >>> 
        >>> def on_notification(notification):
        ...     print(f"New notification: {notification['title']}")
        >>> 
        >>> client = SSEClient(
        ...     base_url='http://localhost:8000',
        ...     profile_token='your-profile-token',
        ...     on_notification=on_notification
        ... )
        >>> 
        >>> # Start listening (blocking)
        >>> client.connect()
        >>> 
        >>> # Or start in background thread
        >>> client.start()
        >>> # ... do other work ...
        >>> client.stop()
    """
    
    def __init__(
        self,
        base_url: str,
        profile_token: str,
        on_notification: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_connect: Optional[Callable[[], None]] = None,
        on_disconnect: Optional[Callable[[], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        reconnect: bool = True,
        reconnect_delay: int = 5,
        timeout: int = 300,
        verify_ssl: bool = True
    ):
        """
        Initialize SSE client
        
        Args:
            base_url: Base URL of Hermes API
            profile_token: Profile access token for authentication
            on_notification: Callback when notification is received
            on_connect: Callback when connection is established
            on_disconnect: Callback when connection is lost
            on_error: Callback when error occurs
            reconnect: Whether to auto-reconnect on disconnect
            reconnect_delay: Seconds to wait before reconnecting
            timeout: SSE connection timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.profile_token = profile_token
        self.on_notification = on_notification
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_error = on_error
        self.reconnect = reconnect
        self.reconnect_delay = reconnect_delay
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._connected = False
        
    def connect(self):
        """
        Connect to SSE stream (blocking)
        
        This method will block until connection is closed or error occurs.
        Use start() for non-blocking connection.
        """
        self._stop_event.clear()
        self._listen()
        
    def start(self):
        """
        Start SSE client in background thread (non-blocking)
        """
        if self._thread and self._thread.is_alive():
            logger.warning("SSE client already running")
            return
            
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()
        logger.info("SSE client started in background")
        
    def stop(self):
        """
        Stop SSE client
        """
        logger.info("Stopping SSE client...")
        self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
            
        self._connected = False
        logger.info("SSE client stopped")
        
    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self._connected
        
    def _listen(self):
        """Main listening loop"""
        while not self._stop_event.is_set():
            try:
                self._connect_and_listen()
            except Exception as e:
                logger.error(f"SSE connection error: {e}")
                
                if self.on_error:
                    try:
                        self.on_error(e)
                    except Exception as callback_error:
                        logger.error(f"Error in on_error callback: {callback_error}")
                
                if not self.reconnect or self._stop_event.is_set():
                    break
                    
                logger.info(f"Reconnecting in {self.reconnect_delay} seconds...")
                self._stop_event.wait(self.reconnect_delay)
                
    def _connect_and_listen(self):
        """Connect to SSE endpoint and listen for events"""
        url = f"{self.base_url}/api/v1/sse/notifications/"
        headers = {
            'Authorization': f'Bearer {self.profile_token}',
            'Accept': 'text/event-stream',
            'Cache-Control': 'no-cache',
        }
        
        logger.info(f"Connecting to SSE: {url}")
        
        try:
            response = requests.get(
                url,
                headers=headers,
                stream=True,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid profile token")
            elif response.status_code != 200:
                raise ConnectionError(f"SSE connection failed: {response.status_code}")
                
            self._connected = True
            logger.info("SSE connection established")
            
            if self.on_connect:
                try:
                    self.on_connect()
                except Exception as e:
                    logger.error(f"Error in on_connect callback: {e}")
            
            # Read SSE stream
            for line in response.iter_lines(decode_unicode=True):
                if self._stop_event.is_set():
                    break
                    
                if not line:
                    continue
                    
                # Parse SSE format: "data: {...}"
                if line.startswith('data: '):
                    data_str = line[6:]  # Remove "data: " prefix
                    
                    try:
                        data = json.loads(data_str)
                        self._handle_event(data)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse SSE data: {e}")
                        
        except requests.exceptions.Timeout:
            raise ConnectionError("SSE connection timeout")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to SSE: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"SSE request failed: {e}")
        finally:
            self._connected = False
            
            if self.on_disconnect:
                try:
                    self.on_disconnect()
                except Exception as e:
                    logger.error(f"Error in on_disconnect callback: {e}")
                    
    def _handle_event(self, data: Dict[str, Any]):
        """Handle SSE event"""
        event_type = data.get('type')
        
        if event_type == 'ping':
            # Heartbeat - ignore
            logger.debug("Received ping")
            return
            
        if event_type == 'notification':
            notification = data.get('data', {})
            logger.info(f"Received notification: {notification.get('id')}")
            
            if self.on_notification:
                try:
                    self.on_notification(notification)
                except Exception as e:
                    logger.error(f"Error in on_notification callback: {e}")
        else:
            logger.warning(f"Unknown event type: {event_type}")


class SSENotificationListener:
    """
    High-level SSE notification listener with built-in notification storage
    
    Example:
        >>> listener = SSENotificationListener(
        ...     base_url='http://localhost:8000',
        ...     profile_token='your-token'
        ... )
        >>> 
        >>> listener.start()
        >>> 
        >>> # Get all received notifications
        >>> notifications = listener.get_notifications()
        >>> 
        >>> # Get unread notifications
        >>> unread = listener.get_notifications(is_read=False)
        >>> 
        >>> # Mark as read
        >>> listener.mark_as_read(notification_id)
        >>> 
        >>> listener.stop()
    """
    
    def __init__(
        self,
        base_url: str,
        profile_token: str,
        max_notifications: int = 100,
        **sse_kwargs
    ):
        """
        Initialize notification listener
        
        Args:
            base_url: Base URL of Hermes API
            profile_token: Profile access token
            max_notifications: Maximum notifications to keep in memory
            **sse_kwargs: Additional arguments for SSEClient
        """
        self.base_url = base_url
        self.profile_token = profile_token
        self.max_notifications = max_notifications
        
        self._notifications: list[Dict[str, Any]] = []
        self._lock = threading.Lock()
        
        self._client = SSEClient(
            base_url=base_url,
            profile_token=profile_token,
            on_notification=self._on_notification,
            **sse_kwargs
        )
        
    def start(self):
        """Start listening for notifications"""
        self._client.start()
        
    def stop(self):
        """Stop listening"""
        self._client.stop()
        
    def is_connected(self) -> bool:
        """Check if connected"""
        return self._client.is_connected()
        
    def _on_notification(self, notification: Dict[str, Any]):
        """Handle incoming notification"""
        with self._lock:
            # Add to beginning of list (newest first)
            self._notifications.insert(0, notification)
            
            # Trim to max size
            if len(self._notifications) > self.max_notifications:
                self._notifications = self._notifications[:self.max_notifications]
                
    def get_notifications(
        self,
        is_read: Optional[bool] = None,
        limit: Optional[int] = None
    ) -> list[Dict[str, Any]]:
        """
        Get stored notifications
        
        Args:
            is_read: Filter by read status (None for all)
            limit: Maximum number to return
            
        Returns:
            List of notifications
        """
        with self._lock:
            notifications = self._notifications.copy()
            
        # Filter by read status
        if is_read is not None:
            notifications = [
                n for n in notifications
                if n.get('is_read') == is_read
            ]
            
        # Apply limit
        if limit:
            notifications = notifications[:limit]
            
        return notifications
        
    def mark_as_read(self, notification_id: str):
        """Mark notification as read in local storage"""
        with self._lock:
            for notification in self._notifications:
                if notification.get('id') == notification_id:
                    notification['is_read'] = True
                    break
                    
    def clear(self):
        """Clear all stored notifications"""
        with self._lock:
            self._notifications.clear()

