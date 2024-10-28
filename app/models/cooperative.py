from app import db
from datetime import datetime

class Cooperative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    members = db.relationship('User', secondary='cooperative_member', backref='cooperatives')
    messages = db.relationship('CooperativeMessage', backref='cooperative', lazy='dynamic')

class CooperativeMember(db.Model):
    __tablename__ = 'cooperative_member'
    cooperative_id = db.Column(db.Integer, db.ForeignKey('cooperative.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class CooperativeMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cooperative_id = db.Column(db.Integer, db.ForeignKey('cooperative.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='cooperative_messages')