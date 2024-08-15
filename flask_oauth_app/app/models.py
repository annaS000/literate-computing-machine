# models.py

from app import db  # Import the db instance from __init__.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(48), unique=True, nullable=False)
    client_secret = db.Column(db.String(120), nullable=False)
    redirect_uri = db.Column(db.String(255), nullable=False)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), unique=True, nullable=False)
    refresh_token = db.Column(db.String(255), unique=True)
    token_type = db.Column(db.String(40))
    expires_at = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.String(48), db.ForeignKey('client.client_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
