from typing import List

from cryptography.fernet import Fernet

from app.config import PASSWORD_ENCRYPTION_KEY
from app.database.models import User


cipher_suite = Fernet(PASSWORD_ENCRYPTION_KEY.encode('utf-8'))

def encrypt_password(password: str) -> str:
    decrypted_password_bytes = password.encode("utf-8")
    encrypted_password_bytes = cipher_suite.encrypt(decrypted_password_bytes)
    return encrypted_password_bytes.decode("utf-8")

def decrypt_password(encrypted_password: str) -> str:
    encrypted_password_bytes = encrypted_password.encode('utf-8')
    decrypted_password_bytes = cipher_suite.decrypt(encrypted_password_bytes)
    return decrypted_password_bytes.decode('utf-8')

def decrypt_users_password(users: List[User]) -> List[User]:
    for user in users:
        encrypted_password_bytes = user.password.encode('utf-8')
        decrypted_password_bytes = cipher_suite.decrypt(encrypted_password_bytes)
        user.password = decrypted_password_bytes.decode('utf-8')
    return users
