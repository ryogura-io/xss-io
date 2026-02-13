from services.sanitization_service import SanitizationService
from services.detection_service import DetectionService
from models.attack_log import AttackLog
from extensions import db
import logging

class SecurityService:
    @staticmethod
    def process_input(text, context='html', ip_address=None, user_agent=None):
        """
        Orchestrates detection, logging, and sanitization.
        Returns the safe, sanitized text.
        """
        
        # 1. Detection
        detection_result = DetectionService.detect_xss(text)
        
        # 2. Logging (if suspicious)
        if detection_result.is_suspicious:
            logging.warning(f"XSS Attempt Detected: Score {detection_result.score}, Rules: {detection_result.matched_rules}")
            
            attack_log = AttackLog(
                payload=text,
                attack_type=detection_result.matched_rules[0] if detection_result.matched_rules else 'unknown',
                risk_score=detection_result.score,
                ip_address=ip_address,
                user_agent=user_agent
            )
            attack_log.set_matched_rules(detection_result.matched_rules)
            
            try:
                db.session.add(attack_log)
                db.session.commit()
            except Exception as e:
                logging.error(f"Failed to log attack: {e}")
                db.session.rollback()

        # 3. Sanitization (ALWAYS)
        sanitized_text = SanitizationService.sanitize_for_context(text, context)
        
        return {
            'original': text,
            'sanitized': sanitized_text,
            'detection': detection_result
        }
