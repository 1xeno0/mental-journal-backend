import os
from dotenv import load_dotenv

# Explicitly load .env file
load_dotenv()

# Ensure data directory exists for local development
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
