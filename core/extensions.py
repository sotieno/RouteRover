from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import os
from dotenv import load_dotenv

# Get the current directory
script_dir = os.path.dirname(__file__)

# Get full path to the .env file in a different directory
dotenv_path = os.path.join(script_dir, '..', '.env')

# Load environment variables from the specified .env file
load_dotenv(dotenv_path)

# Get database connection parameters from environment variables
db_params = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
}
