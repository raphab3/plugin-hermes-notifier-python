"""
Django template tags for Hermes notifications
"""

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import json

register = template.Library()


@register.simple_tag(takes_context=True)
def hermes_sse_script(context, user_id=None):
    """
    Generate JavaScript code for SSE connection to Hermes notifications
    
    Usage in template:
    {% load hermes_tags %}
    {% hermes_sse_script %}
    """
    request = context.get('request')
    if not user_id and request and hasattr(request, 'user'):
        if hasattr(request.user, 'external_user_id'):
            user_id = request.user.external_user_id
        elif hasattr(request.user, 'username'):
            user_id = request.user.username
        else:
            user_id = str(request.user.id)
    
    if not user_id:
        return ""
    
    base_url = getattr(settings, 'HERMES_BASE_URL', 'http://localhost:8000')
    sse_enabled = getattr(settings, 'HERMES_SSE_ENABLED', True)
    
    if not sse_enabled:
        return ""
    
    script = f"""
    <script>
    (function() {{
        var hermesSSE = null;
        var hermesUserId = '{user_id}';
        var hermesBaseUrl = '{base_url}';
        
        function connectHermesSSE() {{
            if (hermesSSE) {{
                hermesSSE.close();
            }}
            
            var sseUrl = hermesBaseUrl + '/sse/notifications/' + encodeURIComponent(hermesUserId) + '/';
            hermesSSE = new EventSource(sseUrl);
            
            hermesSSE.onopen = function() {{
                console.log('Hermes SSE connected');
                if (window.hermesOnConnect) {{
                    window.hermesOnConnect();
                }}
            }};
            
            hermesSSE.onmessage = function(event) {{
                try {{
                    var data = JSON.parse(event.data);
                    if (data.type === 'notification' || data.type === 'new_notification') {{
                        var notification = data.notification || data;
                        if (window.hermesOnNotification) {{
                            window.hermesOnNotification(notification);
                        }} else {{
                            console.log('New notification:', notification);
                        }}
                    }}
                }} catch (e) {{
                    console.warn('Failed to parse Hermes notification:', e);
                }}
            }};
            
            hermesSSE.onerror = function(event) {{
                console.error('Hermes SSE error:', event);
                if (window.hermesOnError) {{
                    window.hermesOnError(event);
                }}
                
                // Reconnect after 5 seconds
                setTimeout(connectHermesSSE, 5000);
            }};
        }}
        
        // Auto-connect when page loads
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', connectHermesSSE);
        }} else {{
            connectHermesSSE();
        }}
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', function() {{
            if (hermesSSE) {{
                hermesSSE.close();
            }}
        }});
        
        // Expose global functions
        window.hermesConnect = connectHermesSSE;
        window.hermesDisconnect = function() {{
            if (hermesSSE) {{
                hermesSSE.close();
                hermesSSE = null;
            }}
        }};
    }})();
    </script>
    """
    
    return mark_safe(script)


@register.simple_tag(takes_context=True)
def hermes_notification_widget(context, max_items=5, show_unread_only=False):
    """
    Render a notification widget with recent notifications
    
    Usage in template:
    {% load hermes_tags %}
    {% hermes_notification_widget max_items=10 show_unread_only=True %}
    """
    notifications = context.get('hermes_notifications', [])
    unread_count = context.get('hermes_unread_count', 0)
    
    if show_unread_only:
        notifications = [n for n in notifications if not n.get('is_read', False)]
    
    notifications = notifications[:max_items]
    
    widget_context = {
        'notifications': notifications,
        'unread_count': unread_count,
        'max_items': max_items,
        'show_unread_only': show_unread_only,
    }
    
    return render_to_string('hermes_notifier/notification_widget.html', widget_context)


@register.simple_tag(takes_context=True)
def hermes_unread_count(context):
    """
    Get the unread notification count
    
    Usage in template:
    {% load hermes_tags %}
    <span class="badge">{% hermes_unread_count %}</span>
    """
    return context.get('hermes_unread_count', 0)


@register.filter
def hermes_priority_class(priority):
    """
    Convert notification priority to CSS class
    
    Usage in template:
    {% load hermes_tags %}
    <div class="notification {{ notification.priority|hermes_priority_class }}">
    """
    class_map = {
        'low': 'notification-low',
        'normal': 'notification-normal', 
        'high': 'notification-high',
        'critical': 'notification-critical',
    }
    return class_map.get(priority, 'notification-normal')


@register.filter
def hermes_time_ago(timestamp):
    """
    Convert timestamp to human-readable time ago format
    
    Usage in template:
    {% load hermes_tags %}
    <span>{{ notification.created_at|hermes_time_ago }}</span>
    """
    from django.utils import timezone
    from datetime import datetime
    
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            return timestamp
    
    if not timestamp:
        return ""
    
    now = timezone.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"


@register.inclusion_tag('hermes_notifier/notification_item.html')
def hermes_notification_item(notification, show_actions=True):
    """
    Render a single notification item
    
    Usage in template:
    {% load hermes_tags %}
    {% hermes_notification_item notification show_actions=True %}
    """
    return {
        'notification': notification,
        'show_actions': show_actions,
    }


@register.simple_tag
def hermes_config_json():
    """
    Generate JSON configuration for client-side JavaScript
    
    Usage in template:
    {% load hermes_tags %}
    <script>
    var hermesConfig = {% hermes_config_json %};
    </script>
    """
    config = {
        'baseUrl': getattr(settings, 'HERMES_BASE_URL', 'http://localhost:8000'),
        'sseEnabled': getattr(settings, 'HERMES_SSE_ENABLED', True),
        'reconnectDelay': getattr(settings, 'HERMES_RECONNECT_DELAY', 5000),
        'maxReconnectAttempts': getattr(settings, 'HERMES_MAX_RECONNECT_ATTEMPTS', 10),
    }
    
    return mark_safe(json.dumps(config))


@register.simple_tag(takes_context=True)
def hermes_notification_count_badge(context, css_class="badge badge-danger"):
    """
    Render unread count as a badge (only if count > 0)
    
    Usage in template:
    {% load hermes_tags %}
    <i class="fa fa-bell"></i>{% hermes_notification_count_badge %}
    """
    count = context.get('hermes_unread_count', 0)
    
    if count > 0:
        return mark_safe(f'<span class="{css_class}">{count}</span>')
    
    return ""