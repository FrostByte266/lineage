import os
from base64 import b64encode

import yaml

flask_secret_key = b64encode(os.urandom(128)).decode('utf-8')
jwt_secret_key = b64encode(os.urandom(128)).decode('utf-8')

try:
    with open('secret_config.yaml') as f:
        parsed_config = yaml.load(f, yaml.BaseLoader)
except FileNotFoundError:
    parsed_config = dict()

parsed_config.update({
    'SECRET_KEY': flask_secret_key,
    'JWT_SECRET_KEY': jwt_secret_key
})


with open('secret_config.yaml', 'w+') as f:
    # yaml.dump(parsed_config, f, yaml.BaseDumper)
    yaml.safe_dump(parsed_config, f)

print('Done')