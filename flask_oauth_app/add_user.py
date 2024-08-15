from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Create the app and push an app context
app = create_app()
with app.app_context():
    # Create a new user
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Hash the password before saving
    hashed_password = generate_password_hash(password)

    # Create the user and add them to the database
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    print(f"User '{username}' created successfully.")
