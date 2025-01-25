from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

from urllib.parse import quote_plus
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("USER")
PASSWORD = quote_plus(os.getenv("PASSWORD"))  # URL-encode the password
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

def email_exists(email_input: str):
    pass