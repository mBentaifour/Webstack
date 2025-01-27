from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from urllib.parse import quote_plus
import os

load_dotenv()

SUPABASE_SECRET_J = os.getenv("SUPABASE_SEC_JWT")
USER = os.getenv("USER")
PASSWORD = quote_plus(os.getenv("PASSWORD"))
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL, poolclass=NullPool)

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

def email_exists(email_input: str):
    """
    Check if an email exists in the auth.users table.
    make sure u pass the email
    Args:
        email_input (str): The email to check.

    Returns:
        bool: True if the email exists, False otherwise.
    """
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM auth.users
            WHERE email = :email_input
        ) AS email_exists;
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {"email_input": email_input})
            return result.scalar()  # Fetch the boolean result
    except Exception as e:
        print(f"Error checking email existence: {e}")
        return False

def check_jwt(token: str) -> bool:
    """
    Verifies the provided JWT token using the Supabase secret.
    
    Args:
        token (str): The JWT token to verify.
    
    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        decoded = jwt.decode(token, SUPABASE_SECRET_J, algorithms=["HS256"])
        print("Decoded Token:", decoded)  # Debugging information
        return True
    except ExpiredSignatureError:
        print("Token has expired.")
        return False
    except InvalidTokenError:
        print("Invalid token.")
        return False
    