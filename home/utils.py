import bcrypt

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
import bcrypt
import jwt
import datetime
from django.conf import settings

# Hash Password Function
def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Verify Password Function
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWT Token Generation
def generate_token(user_id: int) -> str:
    payload = {
        'id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),  # Token expiry after 2 days
        'iat': datetime.datetime.utcnow()  # Issued at time
    }

    # Use a secret key for signing the JWT (store in environment variables or settings for better security)
    secret_key = settings.JWT_SECRET_KEY if hasattr(settings, 'JWT_SECRET_KEY') else 'your_default_secret_key'

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
