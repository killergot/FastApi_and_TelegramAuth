from authlib.jose import jwt


def get_key(secret: str):
    return {'k': secret, 'kty': 'oct'}

def encode_jwt(payload: dict,
            secret: str,
            algorithm: str):
    header = {'alg': algorithm, 'typ': 'JWT'}
    token = jwt.encode(header, payload, get_key(secret)).decode('utf-8')
    return token

def decode_jwt(token: str,
               secret: str):
    try:
        claims = jwt.decode(token, get_key(secret))
        claims.validate()
        return claims
    except:
        return False
