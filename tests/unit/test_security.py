from app.database.models import User
from app.utils.security import (
    decrypt_password,
    decrypt_users_password,
    encrypt_password,
)


def test_encrypt_decrypt_password():
    raw_password = "secret_abc_123"
    encrypted = encrypt_password(raw_password)

    assert encrypted != raw_password
    assert decrypt_password(encrypted) == raw_password

def test_decrypt_users_password_list():
    users = [
        User(id=1, password=encrypt_password("pass1")),
        User(id=2, password=encrypt_password("pass2"))
    ]

    decrypted_users = decrypt_users_password(users)

    assert decrypted_users[0].password == "pass1"
    assert decrypted_users[1].password == "pass2"
