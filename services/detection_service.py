import re

class DetectionResult:
    def __init__(self, is_suspicious=False, score=0, matched_rules=None):
        self.is_suspicious = is_suspicious
        self.score = score
        self.matched_rules = matched_rules or []

class DetectionService:
    PATTERNS = {
        'script_tag': r'<script.*?>.*?</script>',
        'event_handler': r'on\w+\s*=',
        'uri_scheme': r'(javascript|vbscript|data):',
        'iframe': r'<iframe.*?>',
        'object': r'<object.*?>',
        'embed': r'<embed.*?>'
    }

    RISK_SCORES = {
        'script_tag': 10,
        'event_handler': 8,
        'uri_scheme': 9,
        'iframe': 7,
        'object': 7,
        'embed': 7
    }

    @staticmethod
    def detect_xss(text):
        matched_rules = []
        score = 0
        
        for rule_name, pattern in DetectionService.PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                matched_rules.append(rule_name)
                score += DetectionService.RISK_SCORES.get(rule_name, 0)
        
        is_suspicious = score > 0
        
        return DetectionResult(
            is_suspicious=is_suspicious,
            score=score,
            matched_rules=matched_rules
        )
