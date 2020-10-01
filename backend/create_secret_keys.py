import os
from base64 import b64encode

flask_secret_key = b64encode(os.urandom(128)).decode('utf-8')
with open('secret_key.txt', 'w+') as f:
    f.write(flask_secret_key)

jwt_secret_key = b64encode(os.urandom(128)).decode('utf-8')
with open('jwt_secret_key.txt', 'w+') as f:
    f.write(jwt_secret_key)

print('Done')