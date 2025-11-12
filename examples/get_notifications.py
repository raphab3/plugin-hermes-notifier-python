#!/usr/bin/env python3
"""
Example: Get and manage notifications

Usage:
    python get_notifications.py
"""

from hermes_notifier import HermesUnifiedClient

def main():
    # Initialize client
    client = HermesUnifiedClient(
        base_url='http://localhost:8000',
        app_token='your-application-token-here'
    )
    
    user_id = 'user-123'
    
    # Get unread count
    print("📊 Getting notification statistics...\n")
    unread_count = client.get_unread_count(user_id)
    print(f"📬 Unread notifications: {unread_count}")
    
    # Get all notifications
    print("\n📋 Fetching all notifications...")
    all_notifications = client.get_notifications(
        user_id=user_id,
        limit=10
    )
    
    print(f"   Total: {all_notifications['count']}")
    print(f"   Showing: {len(all_notifications['results'])}")
    
    # Display notifications
    print("\n" + "="*60)
    for notification in all_notifications['results']:
        status = "✅ Read" if notification['is_read'] else "📬 Unread"
        print(f"\n{status} - {notification['title']}")
        print(f"   {notification['body']}")
        print(f"   Priority: {notification['priority']}")
        print(f"   Created: {notification['created_at']}")
        print(f"   ID: {notification['id']}")
    
    # Get only unread
    print("\n" + "="*60)
    print("\n📬 Unread notifications only:")
    unread = client.get_notifications(
        user_id=user_id,
        is_read=False,
        limit=5
    )
    
    for notification in unread['results']:
        print(f"   • {notification['title']}")
    
    # Mark first unread as read
    if unread['results']:
        first_unread = unread['results'][0]
        print(f"\n✓ Marking as read: {first_unread['title']}")
        client.mark_as_read(first_unread['id'])
        print("   Done!")
    
    # Get high priority notifications
    print("\n" + "="*60)
    print("\n🔥 High priority notifications:")
    high_priority = client.get_notifications(
        user_id=user_id,
        priority='high',
        limit=5
    )
    
    for notification in high_priority['results']:
        print(f"   • {notification['title']}")
    
    # Mark all as read
    print("\n" + "="*60)
    print("\n✓ Marking all notifications as read...")
    result = client.mark_all_as_read(user_id)
    print(f"   {result.get('message', 'Done!')}")
    
    # Final count
    final_count = client.get_unread_count(user_id)
    print(f"\n📬 Final unread count: {final_count}")

if __name__ == '__main__':
    main()

