from sqlalchemy import func
from extensions import db
from models.attack_log import AttackLog

class AnalyticsService:
    @staticmethod
    def get_total_attacks():
        return db.session.query(func.count(AttackLog.id)).scalar()

    @staticmethod
    def get_attack_distribution():
        """Returns count of attacks per attack type."""
        results = db.session.query(
            AttackLog.attack_type, 
            func.count(AttackLog.id)
        ).group_by(AttackLog.attack_type).all()
        
        return {type_: count for type_, count in results}

    @staticmethod
    def get_recent_attacks(limit=10):
        return AttackLog.query.order_by(AttackLog.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_high_risk_attacks(threshold=8):
        return AttackLog.query.filter(AttackLog.risk_score >= threshold).order_by(AttackLog.timestamp.desc()).all()
