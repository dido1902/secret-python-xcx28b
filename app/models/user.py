from app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile information
    age = db.Column(db.Integer)
    monthly_income = db.Column(db.Float)
    location = db.Column(db.String(100))
    marital_status = db.Column(db.String(20))
    dependents = db.Column(db.Integer)
    
    # Professional information
    employment_status = db.Column(db.String(20))
    years_employed = db.Column(db.Integer)
    sector = db.Column(db.String(50))
    contract_type = db.Column(db.String(20))

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)