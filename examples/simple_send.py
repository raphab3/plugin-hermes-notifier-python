#!/usr/bin/env python3
"""
Simple example: Send a notification

Usage:
    python simple_send.py
"""

from hermes_notifier import HermesUnifiedClient

def main():
    # Initialize client
    client = HermesUnifiedClient(
        base_url='http://localhost:8000',
        app_token='your-application-token-here'
    )
    
    # Send notification
    print("📤 Sending notification...")
    
    result = client.send_notification(
        user_id='user-123',
        title='Welcome! 🎉',
        body='Thanks for joining our platform',
        source_system='example-app',
        priority='normal',
        channels=['email', 'in_app'],
        metadata={
            'action': 'welcome',
            'user_type': 'new'
        }
    )
    
    print(f"✅ Notification sent successfully!")
    print(f"   ID: {result['id']}")
    print(f"   Status: {result.get('status', 'sent')}")
    
    # Get unread count
    count = client.get_unread_count('user-123')
    print(f"\n📬 User has {count} unread notifications")

if __name__ == '__main__':
    main()

