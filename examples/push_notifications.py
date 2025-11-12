#!/usr/bin/env python3
"""
Example: Push notifications with device token registration

Usage:
    python push_notifications.py
"""

from hermes_notifier import HermesUnifiedClient

def main():
    # Initialize client
    client = HermesUnifiedClient(
        base_url='http://localhost:8000',
        app_token='your-application-token-here'
    )
    
    user_id = 'user-123'
    
    # Register device token (FCM/APNS)
    print("📱 Registering device token...")
    
    device_token = 'fcm_token_example_here_from_firebase_sdk'
    
    result = client.register_device_token(
        user_id=user_id,
        device_token=device_token,
        platform='android'  # or 'ios', 'web'
    )
    
    print(f"✅ Device registered!")
    print(f"   {result.get('message', 'Success')}")
    print(f"   Total devices: {result.get('total_devices', 1)}")
    
    # Send push notification
    print("\n📤 Sending push notification...")
    
    notification = client.send_notification(
        user_id=user_id,
        title='New Message 📬',
        body='You have a new message from John',
        source_system='messaging-app',
        priority='high',
        channels=['push', 'in_app'],  # Include 'push' channel
        metadata={
            'message_id': '12345',
            'sender': 'john',
            'action': 'open_message',
            'deep_link': 'myapp://messages/12345'
        }
    )
    
    print(f"✅ Push notification sent!")
    print(f"   ID: {notification['id']}")
    
    # Send push to multiple channels
    print("\n📤 Sending multi-channel notification...")
    
    multi_channel = client.send_notification(
        user_id=user_id,
        title='Order Confirmed 🎉',
        body='Your order #54321 has been confirmed',
        source_system='ecommerce-app',
        priority='normal',
        channels=['push', 'email', 'in_app'],  # All channels
        metadata={
            'order_id': '54321',
            'action': 'view_order',
            'deep_link': 'myapp://orders/54321'
        }
    )
    
    print(f"✅ Multi-channel notification sent!")
    print(f"   ID: {multi_channel['id']}")
    print(f"   Channels: push, email, in_app")
    
    # Unregister device token (optional)
    print("\n🗑️ Unregistering device token...")
    
    unregister_result = client.unregister_device_token(
        user_id=user_id,
        device_token=device_token
    )
    
    print(f"✅ Device unregistered!")
    print(f"   {unregister_result.get('message', 'Success')}")

if __name__ == '__main__':
    main()

