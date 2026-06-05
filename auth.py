from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import base64

load_dotenv()

raw_key = os.getenv("AES_KEY", "12345678901234567890123456789012")

key = base64.urlsafe_b64encode(raw_key.encode().ljust(32, b'0')[:32])

cipher = Fernet(key)

def encrypt_password(password: str):
    encrypted = cipher.encrypt(password.encode())
    return encrypted.decode()

def verify_password(password: str, encrypted_password: str):
    decrypted = cipher.decrypt(encrypted_password.encode()).decode()
    return password == decrypted