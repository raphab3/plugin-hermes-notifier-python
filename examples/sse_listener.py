#!/usr/bin/env python3
"""
SSE Listener example: Receive real-time notifications

Usage:
    python sse_listener.py
"""

import time
from hermes_notifier import HermesUnifiedClient

def on_notification(notification):
    """Called when a new notification arrives"""
    print(f"\n📬 New Notification!")
    print(f"   Title: {notification['title']}")
    print(f"   Body: {notification['body']}")
    print(f"   Priority: {notification.get('priority', 'normal')}")
    print(f"   ID: {notification['id']}")

def on_connect():
    """Called when SSE connection is established"""
    print("✅ Connected to Hermes SSE")

def on_disconnect():
    """Called when SSE connection is lost"""
    print("❌ Disconnected from Hermes SSE")

def on_error(error):
    """Called when an error occurs"""
    print(f"⚠️ Error: {error}")

def main():
    print("🚀 Starting Hermes SSE Listener...")
    print("   Press Ctrl+C to stop\n")
    
    # Initialize client with SSE
    client = HermesUnifiedClient(
        base_url='http://localhost:8000',
        app_token='your-application-token',
        profile_token='your-profile-token',  # Required for SSE
        on_notification=on_notification,
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        on_error=on_error,
        auto_start_sse=True  # Auto-connect
    )
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping SSE listener...")
        client.stop_sse()
        print("✅ Stopped successfully")

if __name__ == '__main__':
    main()

