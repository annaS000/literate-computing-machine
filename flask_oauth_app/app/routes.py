from flask import Blueprint, request, redirect, url_for, jsonify, render_template, session
from authlib.integrations.flask_oauth2 import current_token
from app.auth import authorization
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
import json
from app import db
from authlib.integrations.flask_oauth2 import AuthorizationServer
from functools import wraps
import jwt
import datetime
import openai
import os


bp = Blueprint('routes', __name__)
# CORS(bp)
SECRET_KEY = 'your-secret-key'  # Use a secure secret key

def create_token(user):
    """Generate a JWT token for the authenticated user."""
    payload = {
        'user_id': user.id,  # Unique identifier for the user
        'username': user.username,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            # Decode the token and get the user ID
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated


@bp.route('/authorize', methods=['GET', 'POST'])
def authorize():
    user = User.query.filter_by(id=session.get('user_id')).first()

    if not user:
        return redirect(url_for('routes.login'))

    if request.method == 'POST':
        # Generate a JWT token
        token = create_token(user)
        print(f"Generated Token: {token}")  # Add print statement to confirm token generation
        return jsonify({'token': token})

    return render_template('authorize.html')



@bp.route('/user', methods=['GET'])
def user_profile():
    user = current_token.user
    return jsonify(username=user.username)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('routes.authorize'))
    
    return render_template('login.html')  # You need to create a login form template

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password before saving
        hashed_password = generate_password_hash(password)
        
        # Create the new user and save them to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('routes.login'))

    return render_template('register.html')

# Ensure the OpenAI API key is set in the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@bp.route('/chat', methods=['POST'])
@token_required
def chat(current_user):
    data = request.get_json()
    prompt = data.get('prompt')
    selected_text = data.get('selected_text')

    # Combine the user's prompt with the selected text
    full_prompt = f"Edit the following text: \"{selected_text}\". Prompt: \"{prompt}\""

    try:
        # Make a call to the GPT-4 model via OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Using the GPT-4 model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that edits text."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=150
        )

        # Extract the assistant's response
        ai_response = response['choices'][0]['message']['content'].strip()

        return jsonify({
            'status': 'success',
            'response': ai_response
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

