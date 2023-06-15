import firebase_admin
from fastapi import Depends, HTTPException, Header, Request
from firebase_admin import credentials, auth
import os

print(os.getcwd())
# Path to the service account key JSON file
SERVICE_ACCOUNT_KEY_PATH = os.path.join(os.getcwd(), 'utils/fast-api-server-firebase-adminsdk-f1mv9-190ad6a752.json')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred)


def auth_header(authorization):
    print('ljuhyu',authorization)
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        return token
    print('not found')
    raise HTTPException(status_code=401, detail="Invalid authorization header")


async def get_current_user(authentication):
    try:
        token = auth_header(authentication)
        decoded_token = auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
