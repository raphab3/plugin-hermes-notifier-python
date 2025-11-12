# Hermes Notifier - Python/Django Plugin

> **🚀 Plug-and-play Python client for Hermes Notifications**
>
> Send notifications, manage users, and receive real-time updates with a simple, unified API.

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/raphab3/hermes-notifier-python)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ Features

### Core Features
- 🐍 **Unified Client** - Single client for HTTP API + SSE
- 📬 **Send Notifications** - Email, SMS, Push, In-App
- 📱 **Push Notifications** - FCM/APNS support
- 🔄 **Real-time SSE** - Server-Sent Events for live updates
- 👥 **Group Notifications** - Send to multiple users at once
- 📊 **Notification Management** - Get, filter, mark as read, delete

### Django Integration
- 🌐 **Views Mixin** - Easy integration with Django views
- 🏷️ **Template Tags** - Display notifications in templates
- 🎨 **Pre-built Templates** - Customizable UI components
- ⚙️ **Context Processor** - Auto-inject notifications in templates

### Developer Experience
- ⚡ **Plug-and-play** - Works out of the box
- 🔐 **Token-based auth** - Secure and simple
- 📚 **Rich Examples** - 5+ ready-to-use examples
- 🧪 **Easy Testing** - Mock support included
- 📖 **Great Docs** - Quick start + full reference

---

## 📦 Installation

### Basic Installation

```bash
pip install hermes-notifier
```

### With Django Support

```bash
pip install hermes-notifier[django]
```

### With All Features

```bash
pip install hermes-notifier[all]
```

---

## 🚀 Quick Start

### 1. Send a Notification (3 lines)

```python
from hermes_notifier import HermesUnifiedClient

client = HermesUnifiedClient(
    base_url='http://localhost:8000',
    app_token='your-token'
)

client.send_notification(
    user_id='user-123',
    title='Welcome! 🎉',
    body='Thanks for joining',
    channels=['email', 'in_app']
)
```

### 2. Real-time Notifications (SSE)

```python
def on_notification(notification):
    print(f"📬 {notification['title']}")

client = HermesUnifiedClient(
    base_url='http://localhost:8000',
    app_token='your-app-token',
    profile_token='your-profile-token',
    on_notification=on_notification,
    auto_start_sse=True  # Auto-connect!
)
```

### 3. Get Notifications

```python
# Get unread notifications
notifications = client.get_notifications(
    user_id='user-123',
    is_read=False
)

# Mark as read
client.mark_as_read(notification_id)

# Get unread count
count = client.get_unread_count('user-123')
```

**👉 See [QUICKSTART.md](./QUICKSTART.md) for more examples!**

---

## 📚 Documentation

- **[Quick Start Guide](./QUICKSTART.md)** - Get started in 3 steps
- **[Examples](./examples/)** - 5+ ready-to-use examples
- **[Full API Reference](#api-reference)** - Complete method documentation
- **[Django Integration](#django-integration)** - Django-specific features
- **[Changelog](./CHANGELOG.md)** - Version history

---

## 🎯 Use Cases

### E-commerce
```python
# Order confirmation
client.send_notification(
    user_id='user-123',
    title='Order Confirmed 🎉',
    body='Your order #12345 is confirmed',
    channels=['email', 'push', 'in_app']
)
```

### Social Media
```python
# New follower
client.send_notification(
    user_id='user-123',
    title='New Follower',
    body='John started following you',
    channels=['in_app', 'push'],
    priority='low'
)
```

### Monitoring/Alerts
```python
# Critical alert to team
client.send_group_notification(
    group_id='on-call-team',
    title='🚨 Production Alert',
    body='Database connection pool exhausted',
    channels=['email', 'sms', 'push'],
    priority='critical'
)
```

---

## 📱 Push Notifications

### Register Device Token

```python
# Register FCM/APNS token
client.register_device_token(
    user_id='user-123',
    device_token='fcm_token_here',
    platform='android'  # or 'ios', 'web'
)
```

### Send Push Notification

```python
client.send_notification(
    user_id='user-123',
    title='New Message',
    body='You have a new message',
    channels=['push'],  # ← Push channel
    metadata={
        'deep_link': 'myapp://messages/123'
    }
)
```

**👉 See [examples/push_notifications.py](./examples/push_notifications.py) for complete example!**

---

## Quick Start

### 1. Configure Django Settings

```python
# settings.py

# Required: Hermes API configuration
HERMES_BASE_URL = 'http://localhost:8000'
HERMES_TOKEN = 'your-api-token-here'

# Optional settings
HERMES_DEFAULT_SOURCE = 'my-django-app'
HERMES_TIMEOUT = 30
HERMES_VERIFY_SSL = True
HERMES_RAISE_EXCEPTIONS = False  # Set to True to raise exceptions instead of logging
HERMES_SSE_ENABLED = True
HERMES_USER_ID_FIELD = 'external_user_id'  # Field to use as user ID

# Add context processor for template integration
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... other context processors
                'hermes_notifier.django_integration.hermes_notifications',
            ],
        },
    },
]
```

### 2. Basic Usage in Views

```python
from django.views.generic import TemplateView
from hermes_notifier import HermesNotificationMixin

class MyView(HermesNotificationMixin, TemplateView):
    template_name = 'my_template.html'
    
    def post(self, request, *args, **kwargs):
        # Send a notification
        result = self.send_notification(
            user_id='user-123',
            title='Welcome!',
            body='Thanks for joining our platform',
            priority='normal',
            channels=['email', 'in_app']
        )
        
        if result.get('success'):
            print(f"Notification sent: {result['notification']['id']}")
        
        return self.get(request, *args, **kwargs)
```

### 3. Template Integration

```html
<!-- my_template.html -->
{% load hermes_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
    <!-- Bootstrap for styling (optional) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="#">My App</a>
            
            <!-- Notification bell with unread count -->
            <div class="navbar-nav">
                <a class="nav-link" href="#" data-bs-toggle="dropdown">
                    <i class="fas fa-bell"></i>
                    {% hermes_notification_count_badge %}
                </a>
                
                <!-- Dropdown with notifications -->
                <div class="dropdown-menu dropdown-menu-end">
                    {% hermes_notification_widget max_items=5 %}
                </div>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <h1>Welcome!</h1>
        <p>You have {% hermes_unread_count %} unread notifications.</p>
    </div>
    
    <!-- SSE JavaScript for real-time notifications -->
    {% hermes_sse_script %}
    
    <script>
    // Handle incoming notifications
    window.hermesOnNotification = function(notification) {
        console.log('New notification:', notification);
        
        // Show a toast or update UI
        showToast(notification.title, notification.body);
        
        // Update unread count (you can implement this)
        updateUnreadCount();
    };
    
    function showToast(title, message) {
        // Simple toast implementation
        const toast = document.createElement('div');
        toast.className = 'alert alert-info alert-dismissible fade show position-fixed';
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <strong>${title}</strong><br>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
    </script>
</body>
</html>
```

## API Reference

### HermesNotifier Class

```python
from hermes_notifier import HermesNotifier

# Initialize client
client = HermesNotifier(
    base_url='http://localhost:8000',
    token='your-token',
    timeout=30,
    verify_ssl=True
)

# Send notification
result = client.send_notification(
    user_id='user-123',
    title='Hello',
    body='This is a test notification',
    source_system='my-app',
    priority='normal',
    channels=['email', 'in_app'],
    metadata={'key': 'value'}
)

# Send group notification
result = client.send_group_notification(
    group_id='group-456',
    title='Team Update',
    body='New announcement for the team',
    source_system='my-app'
)

# Get notifications
notifications = client.get_notifications(
    user_id='user-123',
    is_read=False,  # Only unread
    limit=20
)

# Mark as read
result = client.mark_as_read('notification-id')

# Get unread count
count = client.get_unread_count('user-123')

# Validate token
is_valid = client.validate_token()
```

### Django Integration

#### HermesNotificationMixin

Add to any Django view to get notification methods:

```python
from hermes_notifier import HermesNotificationMixin

class MyView(HermesNotificationMixin, View):
    def post(self, request):
        # Send notification
        self.send_notification(
            user_id=request.user.username,
            title='Action Completed',
            body='Your request has been processed'
        )
        
        # Send group notification
        self.send_group_notification(
            group_id='team-leads',
            title='New Task Assigned',
            body='A new task requires your attention'
        )
        
        # Get user notifications
        notifications = self.get_user_notifications(
            user_id=request.user.username,
            is_read=False
        )
        
        # Get unread count
        count = self.get_unread_count(request.user.username)
```

### Template Tags

{% load hermes_tags %}

#### Display Widgets

```html
<!-- Notification widget -->
{% hermes_notification_widget max_items=10 show_unread_only=True %}

<!-- Single notification -->
{% hermes_notification_item notification show_actions=True %}

<!-- Unread count badge -->
<i class="fa fa-bell"></i>{% hermes_notification_count_badge %}

<!-- Just the count -->
<span>{% hermes_unread_count %}</span>
```

#### SSE Integration

```html
<!-- Auto-connect to SSE -->
{% hermes_sse_script %}

<!-- Configuration JSON -->
<script>
var config = {% hermes_config_json %};
</script>
```

#### Filters

```html
<!-- Priority CSS class -->
<div class="{{ notification.priority|hermes_priority_class }}">

<!-- Time ago -->
<span>{{ notification.created_at|hermes_time_ago }}</span>
```

## Configuration Options

### Django Settings

```python
# Required
HERMES_BASE_URL = 'http://localhost:8000'
HERMES_TOKEN = 'your-api-token'

# Optional
HERMES_DEFAULT_SOURCE = 'django-app'  # Default source system name
HERMES_TIMEOUT = 30  # Request timeout in seconds
HERMES_VERIFY_SSL = True  # Verify SSL certificates
HERMES_RAISE_EXCEPTIONS = False  # Raise exceptions vs. logging errors
HERMES_SSE_ENABLED = True  # Enable SSE in templates
HERMES_USER_ID_FIELD = 'external_user_id'  # User model field for user ID
HERMES_CONTEXT_LIMIT = 10  # Max notifications in template context
HERMES_RECONNECT_DELAY = 5000  # SSE reconnect delay (ms)
HERMES_MAX_RECONNECT_ATTEMPTS = 10  # Max SSE reconnect attempts
```

### Environment Variables

You can also use environment variables:

```bash
export HERMES_BASE_URL="http://localhost:8000"
export HERMES_TOKEN="your-token-here"
export HERMES_DEFAULT_SOURCE="my-django-app"
```

## Advanced Usage

### Custom User ID Resolution

```python
# settings.py
HERMES_USER_ID_FIELD = 'profile__external_id'

# Or use a custom function
def get_hermes_user_id(user):
    return f"django_user_{user.id}"

# In your view
class MyView(HermesNotificationMixin, View):
    def get_hermes_user_id(self, user):
        return get_hermes_user_id(user)
```

### Error Handling

```python
from hermes_notifier import HermesNotifierError, AuthenticationError

try:
    result = client.send_notification(
        user_id='user-123',
        title='Test',
        body='Test message'
    )
except AuthenticationError:
    print("Invalid token")
except HermesNotifierError as e:
    print(f"Notification failed: {e}")
```

### Custom Templates

Override the default templates by creating your own:

```
your_app/templates/hermes_notifier/
├── notification_widget.html
├── notification_item.html
└── notification_list.html
```

### Integration with Django Signals

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from hermes_notifier import HermesNotifier

@receiver(post_save, sender=Order)
def notify_order_created(sender, instance, created, **kwargs):
    if created:
        client = HermesNotifier(
            base_url=settings.HERMES_BASE_URL,
            token=settings.HERMES_TOKEN
        )
        
        client.send_notification(
            user_id=instance.user.username,
            title='Order Confirmed',
            body=f'Your order #{instance.id} has been confirmed',
            source_system='e-commerce',
            priority='normal',
            channels=['email', 'in_app']
        )
```

## Testing

### Mock the Client

```python
from unittest.mock import patch, MagicMock
from hermes_notifier import HermesNotifier

def test_notification_sending():
    with patch.object(HermesNotifier, 'send_notification') as mock_send:
        mock_send.return_value = {'success': True, 'notification': {'id': '123'}}
        
        # Your test code here
        result = my_function_that_sends_notification()
        
        assert result['success'] is True
        mock_send.assert_called_once()
```

### Test Views with Mixin

```python
from django.test import TestCase, RequestFactory
from unittest.mock import patch
from myapp.views import MyView

class MyViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
    @patch('hermes_notifier.HermesNotifier.send_notification')
    def test_notification_sent(self, mock_send):
        mock_send.return_value = {'success': True}
        
        request = self.factory.post('/my-endpoint/')
        view = MyView()
        response = view.post(request)
        
        mock_send.assert_called_once()
```

## Examples

See the `test_app/` directory for a complete Django example application demonstrating:

- View integration
- Template usage
- SSE notifications
- Custom styling
- Error handling

## Requirements

- Python 3.8+
- Django 3.2+
- requests 2.25+

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please visit the [GitHub repository](https://github.com/raphab3/hermes-notifier-python).