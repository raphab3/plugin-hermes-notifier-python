# Changelog

All notable changes to the Hermes Notifier Python package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-11-12

### Added

#### New Features
- **HermesUnifiedClient**: New unified client combining HTTP API and SSE in a single interface
- **Push Notifications Support**: 
  - `register_device_token()` method for FCM/APNS token registration
  - `unregister_device_token()` method for token removal
  - Support for push notifications via `channels=['push']`
- **Enhanced Notification Management**:
  - `mark_all_as_read()` method to mark all notifications as read
  - `delete_notification()` method to delete notifications
- **SSE Improvements**:
  - Better error handling and reconnection logic
  - Configurable callbacks for connect/disconnect/error events
  - Auto-start SSE option in unified client

#### Documentation
- **QUICKSTART.md**: New quick start guide with simple examples
- **examples/**: Complete set of ready-to-use examples:
  - `simple_send.py` - Basic notification sending
  - `get_notifications.py` - Fetch and manage notifications
  - `sse_listener.py` - Real-time SSE notifications
  - `push_notifications.py` - Push notification management
  - `group_notifications.py` - Group notifications
  - `examples/README.md` - Comprehensive examples documentation

#### Developer Experience
- `install-local.sh` - Local installation script for development
- Better type hints throughout the codebase
- Improved error messages and logging

### Changed

- **Version**: Bumped to 1.1.0
- **Dependencies**: Made Django optional (install with `pip install hermes-notifier[django]`)
- **Client Initialization**: Simplified with better defaults
- **SSE Client**: Improved stability and reconnection handling

### Improved

- **Error Handling**: More specific exception types (ValidationError, RateLimitError)
- **Documentation**: Comprehensive examples and use cases
- **Code Quality**: Better type hints and docstrings
- **Testing**: Added mock examples for unit testing

### Recommended Migration

**From 1.0.0 to 1.1.0:**

Old way:
```python
from hermes_notifier import HermesNotifier, SSEClient

# Separate clients
http_client = HermesNotifier(base_url, token)
sse_client = SSEClient(base_url, profile_token, on_notification=callback)
sse_client.start()
```

New way (recommended):
```python
from hermes_notifier import HermesUnifiedClient

# Single unified client
client = HermesUnifiedClient(
    base_url=base_url,
    app_token=token,
    profile_token=profile_token,
    on_notification=callback,
    auto_start_sse=True
)
```

**Note**: Old clients (`HermesNotifier`, `SSEClient`) still work and are fully supported!

---

## [1.0.0] - 2025-11-01

### Added

- Initial release
- `HermesNotifier` client for HTTP API
- `SSEClient` for real-time notifications
- `SSENotificationListener` for high-level SSE usage
- Django integration with `HermesNotificationMixin`
- Template tags for Django templates
- Context processor for template integration
- Exception classes for error handling
- Comprehensive README documentation

### Features

- Send notifications to users
- Send group notifications
- Get notifications with filtering
- Mark notifications as read
- Get unread count
- Create notification groups
- Real-time notifications via SSE
- Token validation
- Django views mixin
- Template tags and filters

---

## Release Notes

### v1.1.0 Highlights

🎉 **Major improvements in developer experience!**

- **Unified Client**: No more juggling multiple clients - `HermesUnifiedClient` does it all
- **Push Notifications**: Full support for FCM/APNS push notifications
- **Better Examples**: 5 ready-to-use examples covering all use cases
- **Quick Start**: New QUICKSTART.md gets you running in 3 steps
- **Flexible Installation**: Django is now optional

### Breaking Changes

None! Version 1.1.0 is fully backward compatible with 1.0.0.

### Upgrade Guide

```bash
pip install --upgrade hermes-notifier
```

No code changes required, but we recommend migrating to `HermesUnifiedClient` for new projects.

---

## Future Roadmap

### v1.2.0 (Planned)
- Async/await support with `asyncio`
- Batch notification sending
- Notification templates
- Webhook support
- Enhanced analytics

### v2.0.0 (Future)
- GraphQL support
- WebSocket alternative to SSE
- Built-in notification queue
- Advanced filtering and search
- Notification scheduling

---

## Support

- 📖 [Documentation](./README.md)
- 🚀 [Quick Start](./QUICKSTART.md)
- 📚 [Examples](./examples/)
- 🐛 [Report Issues](https://github.com/raphab3/hermes-notifier-python/issues)
- 💬 [Discussions](https://github.com/raphab3/hermes-notifier-python/discussions)

