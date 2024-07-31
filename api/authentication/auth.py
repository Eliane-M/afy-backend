# import requests
from django.contrib.auth.models import User
import jwt
from django.conf import settings
from core.settings import SECRET_KEY

def verify_user(access_token_with_bearer):
    if not access_token_with_bearer or not access_token_with_bearer.startswith("Bearer "):
        return None, "Invalid token format. Expected 'Bearer <token>'"
    
    access_token = access_token_with_bearer.split()[1]

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                return user, "User verified"
            except User.DoesNotExist:
                return None, "User does not exist"
        return None, "Invalid payload in token"
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

