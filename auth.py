from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
from dotenv import load_dotenv
import base64

load_dotenv()

AES_KEY = os.getenv("AES_KEY").encode()

def encrypt_password(password: str):
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(AES_KEY),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()

    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(iv + encrypted).decode()

def verify_password(password: str, encrypted_password: str):
    data = base64.b64decode(encrypted_password)

    iv = data[:16]
    encrypted = data[16:]

    cipher = Cipher(
        algorithms.AES(AES_KEY),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    padded_data = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()

    decrypted = (
        unpadder.update(padded_data)
        + unpadder.finalize()
    ).decode()

    return password == decrypted