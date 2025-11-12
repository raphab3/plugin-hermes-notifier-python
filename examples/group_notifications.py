#!/usr/bin/env python3
"""
Example: Group notifications

Usage:
    python group_notifications.py
"""

from hermes_notifier import HermesUnifiedClient

def main():
    # Initialize client
    client = HermesUnifiedClient(
        base_url='http://localhost:8000',
        app_token='your-application-token-here'
    )
    
    # Create a group
    print("👥 Creating notification group...")
    
    group = client.create_group(
        name='Team Leads',
        description='All team leaders in the organization',
        member_ids=['user-1', 'user-2', 'user-3', 'user-4']
    )
    
    print(f"✅ Group created!")
    print(f"   ID: {group['id']}")
    print(f"   Name: {group['name']}")
    print(f"   Members: {len(group.get('members', []))}")
    
    # Send notification to group
    print("\n📤 Sending notification to group...")
    
    result = client.send_group_notification(
        group_id=group['id'],
        title='Team Meeting 📅',
        body='Team meeting scheduled for tomorrow at 3 PM',
        source_system='calendar-app',
        priority='normal',
        channels=['email', 'in_app'],
        metadata={
            'meeting_id': 'meeting-123',
            'date': '2025-11-13',
            'time': '15:00',
            'location': 'Conference Room A'
        }
    )
    
    print(f"✅ Group notification sent!")
    print(f"   Notification ID: {result['notification_id']}")
    print(f"   Recipients: {result.get('recipients_count', 0)}")
    
    # Send urgent notification to group
    print("\n📤 Sending urgent notification to group...")
    
    urgent = client.send_group_notification(
        group_id=group['id'],
        title='🚨 System Alert',
        body='Production server experiencing high load',
        source_system='monitoring-app',
        priority='critical',
        channels=['email', 'sms', 'push', 'in_app'],
        metadata={
            'alert_type': 'high_load',
            'server': 'prod-01',
            'cpu_usage': '95%'
        }
    )
    
    print(f"✅ Urgent notification sent!")
    print(f"   All channels: email, sms, push, in_app")

if __name__ == '__main__':
    main()

