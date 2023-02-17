import binascii
import os
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)
import base64
import bcrypt

class BasicAuthMiddlewareBackend(AuthenticationBackend):
    def __init__(self) -> None:
        super().__init__()
        if not os.path.exists('.htpasswd'):
            raise FileExistsError('File .htpasswd does not exists')
        htpasswd = list(map(lambda x: x.split(':'), open('.htpasswd', 'r').readlines()))
        self.htpasswd = {}
        for item in htpasswd:
            self.htpasswd[item[0]] = item[1].rstrip('\n')


    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            raise AuthenticationError('Invalid basic auth credentials')

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
            print(decoded)
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        hashed_pass = self.htpasswd.get(username, False)

        if hashed_pass and bcrypt.checkpw(password.encode(), hashed_pass.encode()):
            return AuthCredentials(["authenticated"]), SimpleUser(username)
        else:
            raise AuthenticationError('Incorrect basic auth credentials')