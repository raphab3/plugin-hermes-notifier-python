# 📚 Hermes Notifier - Python Examples

Ready-to-use examples demonstrating all features of the Hermes Notifier Python client.

---

## 🚀 Quick Start

### 1. Install the package

```bash
pip install hermes-notifier
```

### 2. Configure your credentials

Edit each example file and replace:
- `your-application-token-here` with your actual application token
- `your-profile-token` with your actual profile token (for SSE examples)
- `http://localhost:8000` with your Hermes API URL

### 3. Run an example

```bash
python simple_send.py
```

---

## 📋 Available Examples

### **1. simple_send.py** - Basic notification sending

**What it does:**
- Initializes Hermes client
- Sends a simple notification
- Gets unread count

**Run:**
```bash
python simple_send.py
```

**Output:**
```
📤 Sending notification...
✅ Notification sent successfully!
   ID: 123e4567-e89b-12d3-a456-426614174000
   Status: sent

📬 User has 5 unread notifications
```

---

### **2. get_notifications.py** - Fetch and manage notifications

**What it does:**
- Gets all notifications
- Filters by read status
- Filters by priority
- Marks notifications as read
- Marks all as read

**Run:**
```bash
python get_notifications.py
```

**Output:**
```
📊 Getting notification statistics...

📬 Unread notifications: 5

📋 Fetching all notifications...
   Total: 25
   Showing: 10

============================================================

📬 Unread - Welcome! 🎉
   Thanks for joining our platform
   Priority: normal
   Created: 2025-11-12T10:30:00Z
   ID: 123e4567-e89b-12d3-a456-426614174000

...
```

---

### **3. sse_listener.py** - Real-time notifications via SSE

**What it does:**
- Connects to Hermes SSE
- Listens for real-time notifications
- Displays notifications as they arrive
- Handles connection events

**Run:**
```bash
python sse_listener.py
```

**Output:**
```
🚀 Starting Hermes SSE Listener...
   Press Ctrl+C to stop

✅ Connected to Hermes SSE

📬 New Notification!
   Title: New Message
   Body: You have a new message from John
   Priority: normal
   ID: 123e4567-e89b-12d3-a456-426614174000

...
```

**Note:** Keep this running to receive notifications in real-time!

---

### **4. push_notifications.py** - Push notification management

**What it does:**
- Registers device token (FCM/APNS)
- Sends push notifications
- Sends multi-channel notifications
- Unregisters device token

**Run:**
```bash
python push_notifications.py
```

**Output:**
```
📱 Registering device token...
✅ Device registered!
   Device token registered successfully
   Total devices: 1

📤 Sending push notification...
✅ Push notification sent!
   ID: 123e4567-e89b-12d3-a456-426614174000

📤 Sending multi-channel notification...
✅ Multi-channel notification sent!
   ID: 456e7890-e89b-12d3-a456-426614174001
   Channels: push, email, in_app
```

---

### **5. group_notifications.py** - Group notification management

**What it does:**
- Creates notification groups
- Sends notifications to groups
- Sends urgent notifications to groups

**Run:**
```bash
python group_notifications.py
```

**Output:**
```
👥 Creating notification group...
✅ Group created!
   ID: group-123
   Name: Team Leads
   Members: 4

📤 Sending notification to group...
✅ Group notification sent!
   Notification ID: 123e4567-e89b-12d3-a456-426614174000
   Recipients: 4
```

---

## 🔧 Configuration

### Environment Variables (Recommended)

Create a `.env` file:

```bash
HERMES_BASE_URL=http://localhost:8000
HERMES_APP_TOKEN=your-application-token
HERMES_PROFILE_TOKEN=your-profile-token
```

Then use in your code:

```python
import os
from dotenv import load_dotenv
from hermes_notifier import HermesUnifiedClient

load_dotenv()

client = HermesUnifiedClient(
    base_url=os.getenv('HERMES_BASE_URL'),
    app_token=os.getenv('HERMES_APP_TOKEN'),
    profile_token=os.getenv('HERMES_PROFILE_TOKEN')
)
```

### Direct Configuration

```python
from hermes_notifier import HermesUnifiedClient

client = HermesUnifiedClient(
    base_url='http://localhost:8000',
    app_token='your-application-token',
    profile_token='your-profile-token'  # Optional, for SSE
)
```

---

## 🎯 Use Cases

### **E-commerce Application**

```python
# Order confirmation
client.send_notification(
    user_id=order.user_id,
    title='Order Confirmed 🎉',
    body=f'Your order #{order.id} has been confirmed',
    channels=['email', 'push', 'in_app'],
    metadata={'order_id': order.id}
)

# Shipping update
client.send_notification(
    user_id=order.user_id,
    title='Order Shipped 📦',
    body=f'Your order is on the way!',
    channels=['push', 'in_app'],
    metadata={'tracking_number': order.tracking}
)
```

### **Social Media Application**

```python
# New follower
client.send_notification(
    user_id=user.id,
    title='New Follower',
    body=f'{follower.name} started following you',
    channels=['in_app', 'push'],
    priority='low'
)

# New comment
client.send_notification(
    user_id=post.author_id,
    title='New Comment',
    body=f'{commenter.name} commented on your post',
    channels=['in_app', 'push'],
    priority='normal'
)
```

### **Monitoring/Alert System**

```python
# Critical alert
client.send_group_notification(
    group_id='on-call-engineers',
    title='🚨 Production Alert',
    body='Database connection pool exhausted',
    channels=['email', 'sms', 'push'],
    priority='critical',
    metadata={
        'severity': 'critical',
        'service': 'database',
        'action_required': True
    }
)
```

---

## 🧪 Testing

### Mock the Client

```python
from unittest.mock import patch, MagicMock

def test_send_notification():
    with patch('hermes_notifier.HermesUnifiedClient') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.send_notification.return_value = {
            'id': '123',
            'status': 'sent'
        }
        
        # Your test code here
        result = send_welcome_notification('user-123')
        
        assert result['status'] == 'sent'
        mock_instance.send_notification.assert_called_once()
```

---

## 📚 Additional Resources

- [Quick Start Guide](../QUICKSTART.md)
- [Full Documentation](../README.md)
- [API Reference](../README.md#api-reference)
- [Django Integration](../README.md#django-integration)

---

## 🆘 Troubleshooting

### Connection Error

```
❌ Failed to connect to Hermes API
```

**Solution:** Check that:
- Hermes API is running
- `base_url` is correct
- Network connectivity is working

### Authentication Error

```
❌ Invalid token
```

**Solution:** Check that:
- Application token is valid
- Token has not expired
- Token has correct permissions

### SSE Not Connecting

```
❌ SSE connection failed
```

**Solution:** Check that:
- Profile token is provided
- Profile token is valid
- SSE endpoint is accessible

---

## 💡 Tips

✅ **Use environment variables** for credentials  
✅ **Handle exceptions** in production code  
✅ **Use `auto_start_sse=True`** for automatic SSE connection  
✅ **Set appropriate priorities** for different notification types  
✅ **Use metadata** to pass additional context  

---

**Happy coding! 🚀**

