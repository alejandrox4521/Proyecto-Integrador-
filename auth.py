import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

PEPPER = os.getenv("PEPPER", "pepper_de_prueba")


def hash_password(password: str):
    password_peppered = (password + PEPPER).encode()
    hashed = bcrypt.hashpw(password_peppered, bcrypt.gensalt())
    return hashed.decode()


def verify_password(password: str, hashed_password: str):
    password_peppered = (password + PEPPER).encode()
    return bcrypt.checkpw(password_peppered, hashed_password.encode())