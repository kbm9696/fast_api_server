import logging

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from firebase_admin import auth
from utils.firebase_auth import SERVICE_ACCOUNT_KEY_PATH
import pyrebase
import json

firebaseConfig = {
    'apiKey': "AIzaSyAeiyMUQ1Q150AAILYKSEJZgNSJSol79zU",
    'authDomain': "fast-api-server.firebaseapp.com",
    'projectId': "fast-api-server",
    'storageBucket': "fast-api-server.appspot.com",
    'messagingSenderId': "1084547978717",
    'appId': "1:1084547978717:web:b7480da11ac7a053311234",
    'measurementId': "G-RY32WJFH70",
    'databaseURL': ""
}

pd = pyrebase.initialize_app(firebaseConfig)


class SignUp:

    def post(self, data):
        try:
            logging.info('Creating new user')
            # Create a new user with the provided email and password
            user = auth.create_user(email=data['email'], password=data['password'])
            return JSONResponse(content={'message': f'Successfully created user {user.uid}'}, status_code=200)
        except Exception as e:
            # Handle any errors that occur during user creation
            raise HTTPException(status_code=400, detail="User creation failed: " + str(e))


class LogIn:

    def post(self, data):
        try:
            logging.info('processing login...')
            user = auth.get_user_by_email(data['email'])
            u = pd.auth().sign_in_with_email_and_password(data['email'], data['password'])
            token = u['idToken']
            res = {'auth_token': token}
            return JSONResponse(content=res, status_code=201)
        except Exception as e:
            # Handle any authentication error
            logging.error(f"Error while login: {e}")
            return JSONResponse(content={'Error':'Cant able to login}'}, status_code=400)
