import hashlib
import secrets
import hmac
import time

SECRET_KEY = "campuscare22_jwt_secret_key_change_in_production"

def hash_password(password: str) -> str:
    """Hashes a plain password using PBKDF2 HMAC SHA256 with a random salt."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}:{pwd_hash}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against stored salt:hash string."""
    if not hashed_password:
        return False
    
    # Handle plain text fallback for initial seed demo users if unhashed
    if ":" not in hashed_password:
        return plain_password == hashed_password

    try:
        salt, stored_hash = hashed_password.split(":", 1)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return hmac.compare_digest(pwd_hash, stored_hash)
    except Exception:
        return False

def generate_session_token(user_id: int, role: str) -> str:
    """Generates a secure timestamped session token."""
    timestamp = int(time.time())
    raw = f"{user_id}:{role}:{timestamp}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), raw.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"{raw}:{signature}"

def verify_session_token(token: str) -> bool:
    """Validates session token signature."""
    try:
        parts = token.split(":")
        if len(parts) != 4:
            return False
        user_id, role, timestamp, signature = parts
        raw = f"{user_id}:{role}:{timestamp}"
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), raw.encode('utf-8'), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected_sig)
    except Exception:
        return False
