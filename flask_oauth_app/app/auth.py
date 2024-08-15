from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from app.models import db, User, Client, Token
from flask import current_app
import datetime
authorization = AuthorizationServer()

def config_oauth(app):
    authorization.init_app(app, query_client=query_client, save_token=save_token)

def query_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

def save_token(token_data, request):
    token = Token(
        access_token=token_data['access_token'],
        refresh_token=token_data.get('refresh_token'),
        token_type=token_data['token_type'],
        expires_at=datetime.utcfromtimestamp(token_data['expires_at']),
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    db.session.add(token)
    db.session.commit()

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def create_authorization_code(self, client, grant_user):
        # Logic to generate the authorization code
        pass

    def parse_authorization_code(self, code, client):
        # Logic to parse the authorization code
        pass

authorization.register_grant(AuthorizationCodeGrant)
