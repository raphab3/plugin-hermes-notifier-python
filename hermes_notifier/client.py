"""
Main Hermes Notifier client for Python applications
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
import requests
from .exceptions import HermesNotifierError, AuthenticationError, ConnectionError, ValidationError, RateLimitError

logger = logging.getLogger(__name__)


class HermesNotifier:
    """
    Python client for the Hermes notifications system
    """
    
    def __init__(
        self, 
        base_url: str, 
        token: str,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize the Hermes notifier client
        
        Args:
            base_url: Base URL of the Hermes API (e.g., 'http://localhost:8000')
            token: Authentication token
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Set up session with default headers
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'hermes-notifier-python/1.0.0'
        })
        
    def send_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        source_system: str,
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
            source_system: System that generated the notification
            priority: Priority level ('low', 'normal', 'high', 'critical')
            channels: List of channels to send through (default: ['email'])
            metadata: Additional metadata dictionary
            
        Returns:
            Dictionary with notification details
            
        Raises:
            AuthenticationError: If authentication fails
            ValidationError: If request validation fails
            RateLimitError: If rate limit is exceeded
            ConnectionError: If connection fails
        """
        if channels is None:
            channels = ['email']
            
        if metadata is None:
            metadata = {}
            
        data = {
            'user_id': user_id,
            'title': title,
            'body': body,
            'source_system': source_system,
            'priority': priority,
            'channels': channels,
            'metadata': metadata
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/notifications/',
                json=data,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")
    
    def send_group_notification(
        self,
        group_id: str,
        title: str,
        body: str,
        source_system: str,
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
            channels: List of channels to send through (default: ['email'])
            metadata: Additional metadata dictionary
            
        Returns:
            Dictionary with group notification results
        """
        if channels is None:
            channels = ['email']
            
        if metadata is None:
            metadata = {}
            
        data = {
            'group_id': group_id,
            'title': title,
            'body': body,
            'source_system': source_system,
            'priority': priority,
            'channels': channels,
            'metadata': metadata
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/groups/send-notification/',
                json=data,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")
    
    def get_notifications(
        self,
        user_id: str,
        is_read: Optional[bool] = None,
        priority: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get notifications for a user
        
        Args:
            user_id: ID of the user
            is_read: Filter by read status (None for all)
            priority: Filter by priority level
            limit: Number of notifications to return
            offset: Offset for pagination
            
        Returns:
            Dictionary with notifications and pagination info
        """
        params = {
            'user_id': user_id,
            'limit': limit,
            'offset': offset
        }
        
        if is_read is not None:
            params['is_read'] = 'true' if is_read else 'false'
            
        if priority:
            params['priority'] = priority
        
        try:
            response = self.session.get(
                f'{self.base_url}/api/v1/notifications/',
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")
    
    def mark_as_read(self, notification_id: str) -> Dict[str, Any]:
        """
        Mark a notification as read
        
        Args:
            notification_id: ID of the notification to mark as read
            
        Returns:
            Dictionary with operation result
        """
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/notifications/{notification_id}/mark_as_read/',
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")
    
    def get_unread_count(self, user_id: str) -> int:
        """
        Get count of unread notifications for a user

        Args:
            user_id: ID of the user

        Returns:
            Number of unread notifications
        """
        try:
            response = self.session.get(
                f'{self.base_url}/api/v1/notifications/unread_count/',
                params={'user_id': user_id},
                timeout=self.timeout,
                verify=self.verify_ssl
            )

            data = self._handle_response(response)
            return data.get('unread_count', 0)

        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")

    def mark_all_as_read(self, user_id: str) -> Dict[str, Any]:
        """
        Mark all notifications as read for a user

        Args:
            user_id: ID of the user

        Returns:
            Dictionary with operation result
        """
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/notifications/mark_all_as_read/',
                json={'user_id': user_id},
                timeout=self.timeout,
                verify=self.verify_ssl
            )

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")

    def delete_notification(self, notification_id: str) -> Dict[str, Any]:
        """
        Delete a notification

        Args:
            notification_id: ID of the notification to delete

        Returns:
            Dictionary with operation result
        """
        try:
            response = self.session.delete(
                f'{self.base_url}/api/v1/notifications/{notification_id}/',
                timeout=self.timeout,
                verify=self.verify_ssl
            )

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")

    def register_device_token(
        self,
        user_id: str,
        device_token: str,
        platform: str = 'unknown'
    ) -> Dict[str, Any]:
        """
        Register a device token for push notifications

        Args:
            user_id: External user ID
            device_token: FCM/APNS device token
            platform: Platform type ('ios', 'android', 'web')

        Returns:
            Dictionary with registration result
        """
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/profiles/{user_id}/register-device/',
                json={
                    'device_token': device_token,
                    'platform': platform
                },
                timeout=self.timeout,
                verify=self.verify_ssl
            )

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")

    def unregister_device_token(
        self,
        user_id: str,
        device_token: str
    ) -> Dict[str, Any]:
        """
        Unregister a device token

        Args:
            user_id: External user ID
            device_token: FCM/APNS device token to remove

        Returns:
            Dictionary with unregistration result
        """
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/profiles/{user_id}/unregister-device/',
                json={'device_token': device_token},
                timeout=self.timeout,
                verify=self.verify_ssl
            )

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")
    
    def create_group(
        self,
        name: str,
        description: str = '',
        member_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a notification group
        
        Args:
            name: Group name
            description: Group description
            member_ids: List of user profile IDs to add as members
            
        Returns:
            Dictionary with group details
        """
        data = {
            'name': name,
            'description': description,
            'members': member_ids or []
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/groups/',
                json=data,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Hermes API: {e}")
        except requests.exceptions.RequestException as e:
            raise HermesNotifierError(f"Request failed: {e}")
    
    def validate_token(self) -> bool:
        """
        Validate the current authentication token
        
        Returns:
            True if token is valid, False otherwise
        """
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/tokens/validate_token/',
                json={'token': self.token},
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            data = self._handle_response(response)
            return data.get('valid', False)
            
        except (AuthenticationError, ValidationError):
            return False
        except requests.exceptions.RequestException:
            return False
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions
        
        Args:
            response: Requests response object
            
        Returns:
            Parsed JSON response data
            
        Raises:
            AuthenticationError: If authentication fails (401)
            ValidationError: If validation fails (400)
            RateLimitError: If rate limit exceeded (429)
            HermesNotifierError: For other HTTP errors
        """
        try:
            # Try to parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = {'error': 'Invalid JSON response'}
            
            if response.status_code == 200 or response.status_code == 201:
                return data
            elif response.status_code == 400:
                error_msg = data.get('error', 'Validation error')
                raise ValidationError(error_msg)
            elif response.status_code == 401:
                error_msg = data.get('error', 'Authentication failed')
                raise AuthenticationError(error_msg)
            elif response.status_code == 403:
                error_msg = data.get('error', 'Permission denied')
                raise AuthenticationError(error_msg)
            elif response.status_code == 429:
                error_msg = data.get('error', 'Rate limit exceeded')
                retry_after = response.headers.get('Retry-After')
                raise RateLimitError(error_msg, retry_after)
            else:
                error_msg = data.get('error', f'HTTP {response.status_code}')
                raise HermesNotifierError(f"API error: {error_msg}")
                
        except requests.exceptions.JSONDecodeError:
            raise HermesNotifierError(f"Invalid response: HTTP {response.status_code}")
    
    def __repr__(self):
        return f"HermesNotifier(base_url='{self.base_url}')"