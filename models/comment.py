from datetime import datetime
from extensions import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    raw_text = db.Column(db.Text, nullable=False)  # For research/logging only
    sanitized_text = db.Column(db.Text, nullable=False)
    context = db.Column(db.String(50), default='html') # html, js, url, etc.
    is_flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id}>'
