import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from workflow import Role


SECRET = os.environ.get("SECRET", "dev-secret-abhisheksharma")
ALGO = "HS256"

USERS = {
    "suresh": {"password": "demo123", "name": "Suresh", "role": Role.VILLAGE_ACCOUNTANT},
    "meena": {"password": "demo123", "name": "Meena", "role": Role.REVENUE_INSPECTOR},
    "rao": {"password": "demo123", "name": "Rao Sahab", "role": Role.TAHSILDAR},
}

bearer = HTTPBearer()


def create_token(username: str) -> str:
    payload = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(hours=8)}
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(creds.credentials, SECRET, algorithms=[ALGO])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


    username = payload.get("sub")
    user = USERS.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Unknown user")

    return {"username": username, **user}

