from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app, resources={r"/*": {"origins": ["https://localhost:3000", "https://localhost:5000"]}})


if __name__ == '__main__':
   app.run(ssl_context=('adhoc'), debug=True)

