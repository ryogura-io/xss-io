import bleach
import json
import urllib.parse

class SanitizationService:
    @staticmethod
    def sanitize_html(text):
        """Allow only safe HTML tags and attributes."""
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br']
        allowed_attrs = {
            'a': ['href', 'title']
        }
        return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    @staticmethod
    def encode_js(text):
        """Encode text for safe insertion into JavaScript strings."""
        # Simple JSON encoding is often sufficient for string contexts
        return json.dumps(text)[1:-1] 

    @staticmethod
    def encode_url(text):
        """Encode text for safe use in URLs."""
        return urllib.parse.quote(text)

    @staticmethod
    def sanitize_for_context(text, context='html'):
        """Dispatch sanitization based on context."""
        if context == 'html':
            return SanitizationService.sanitize_html(text)
        elif context == 'js':
            return SanitizationService.encode_js(text)
        elif context == 'url':
            return SanitizationService.encode_url(text)
        else:
            # Default to harmless string if unknown
            return bleach.clean(text)
