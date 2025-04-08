import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Use a static key for now (in production, use env var)
SECRET_KEY = b'0123456789abcdef0123456789abcdef'  # Must be 32 bytes

def encrypt_password(plain_text):
    aesgcm = AESGCM(SECRET_KEY)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plain_text.encode(), None)
    encrypted = base64.b64encode(nonce + ct).decode()
    return encrypted

def decrypt_password(encrypted_text):
    try:
        raw = base64.b64decode(encrypted_text)
        nonce = raw[:12]
        ct = raw[12:]
        aesgcm = AESGCM(SECRET_KEY)
        decrypted = aesgcm.decrypt(nonce, ct, None)
        return decrypted.decode()
    except Exception as e:
        print("Decryption failed:", e)
        return None
