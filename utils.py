import jwt
import datetime

SECRET_KEY = 'clave-supersecreta'

def generate_dynamic_token(user_id, duration_minutes=5):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=duration_minutes)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_dynamic_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
