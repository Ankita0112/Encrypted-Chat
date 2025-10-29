"""
Containes all the minor independent functions
"""

# Clean Email
def clean_email(email: str):
    local_part, domain = email.split('@')
    cleaned_local_part = local_part.split('+')[0]
    cleaned_email = f"{cleaned_local_part}@{domain}"
    return cleaned_email.lower()


# Calculation SHA256 Hash
import hashlib
sha256 = lambda input: hashlib.sha256(input.encode()).hexdigest()


# JWT Token Functions
import jwt
from config import  JWT_SECRET, JWT_ALGORITHM

def is_jwt(jwt_token):
    try:
        # Check if the token has 3 parts separated by '.'
        if jwt_token.count('.') != 2:
            return False

        # Decode the JWT token without verifying signature (just to check structure)
        jwt.decode(jwt_token, options={"verify_signature": False})
        return True
    except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False
    
# Checks if cookies/auth_token has all the required feilds
check_auth = lambda auth_token: True if auth_token.get('user_id', None) else False

jwt_encode = lambda payload: jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)

def jwt_decode(jwt_token: str):
    if is_jwt(jwt_token):
        auth_token = jwt.decode(jwt=jwt_token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        if check_auth(auth_token=auth_token):
            return True, auth_token

    return False, ''



# Generates Form-ID
import random
uuid_pool = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
generate_uuid = lambda: ''.join(random.choice(uuid_pool) for _ in range(5))

# Chat and Message ID
generate_message_id = lambda: ''.join(random.choice(uuid_pool) for _ in range(8))
generate_chat_id = lambda: ''.join(random.choice(uuid_pool) for _ in range(6))
generate_session_id = lambda: ''.join(random.choice(uuid_pool) for _ in range(10))

# Generate Verification_id
import re
generate_verification_id = lambda: generate_uuid()+'-'+generate_uuid()+generate_uuid()+'-'+generate_uuid()

def is_valid_verification_id(verification_id: str):
    pattern = r"^[a-zA-Z0-9]{5}-[a-zA-Z0-9]{10}-[a-zA-Z0-9]{5}$"
    return bool(re.fullmatch(pattern, verification_id))

# Manages Time with time-zone
from datetime import datetime, timedelta, timezone
def datetime_form_datetime_str(datetime_str):
    """
    Parse a variety of datetime string formats and return a datetime object.
    Accepts:
      - datetime objects (returned unchanged)
      - ISO 8601 (e.g. 2025-11-19T17:59:20+00:00)
      - 'YYYY-mm-dd HH:MM:SS%z'
      - 'YYYY-mm-dd HH:MM:SS'
      - 'YYYY-mm-ddTHH:MM:SS(.microseconds)(%z)'
    """
    if isinstance(datetime_str, datetime):
        return datetime_str

    if datetime_str is None:
        raise ValueError("datetime_str is None")

    # try the flexible ISO parser first
    try:
        return datetime.fromisoformat(datetime_str)
    except Exception:
        pass

    # fallback formats
    formats = [
        '%Y-%m-%d %H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f%z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except Exception:
            continue

    raise ValueError(f"time data {datetime_str!r} does not match expected formats")

def current_time():
    return datetime.now(timezone.utc)

def one_day_form_now():
    new_datetime = datetime.now(timezone.utc) + timedelta(days=1)
    return new_datetime.strftime("%Y-%m-%d %H:%M:%S%z")

def one_month_form_now():
    new_datetime = datetime.now(timezone.utc) + timedelta(weeks=4)
    return new_datetime.strftime("%Y-%m-%d %H:%M:%S%z")
