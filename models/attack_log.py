from datetime import datetime
from extensions import db
import json

class AttackLog(db.Model):
    __tablename__ = 'attack_logs'

    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Text, nullable=False)
    attack_type = db.Column(db.String(50)) # script-tag, event-handler, uri-scheme
    risk_score = db.Column(db.Integer)
    matched_rules = db.Column(db.Text) # Stored as JSON string
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def set_matched_rules(self, rules):
        self.matched_rules = json.dumps(rules)

    def get_matched_rules(self):
        return json.loads(self.matched_rules) if self.matched_rules else []

    def __repr__(self):
        return f'<AttackLog {self.id} - {self.attack_type}>'
