# Authentication

# Generating RSA Keys
1. ``openssl genpkey -algorithm RSA -out private_key.pem``
2. ``openssl rsa -pubout -in private_key.pem -out public_key.pem``

# Generating key to encrypt user id
1. ``import secrets ``
2. ``import base64 key = secrets.token_bytes(32) # used to generate 32 byte (256) key``
3. ``key_string = base64 b64encode(key).decode('utf-8')``
