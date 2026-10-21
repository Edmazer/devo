from app import db, lm
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint, CheckConstraint

@lm.user_loader
def load_user(user_id):
    return User_model.query.get(user_id)

class User_model(db.Model, UserMixin):
    """Model para conta de usuários."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String(40),  unique=True, nullable=False)
    trabalho = db.Column(db.String(40), nullable=False)
    salario = db.Column(db.String, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
