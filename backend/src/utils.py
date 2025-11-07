from datetime import datetime, timedelta

import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_token(username: str):
    expire = datetime.now() + timedelta(hours=1)
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
