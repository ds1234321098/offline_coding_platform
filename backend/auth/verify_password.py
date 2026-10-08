import bcrypt
def verify_entered_password(plain: str, stored: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), stored.encode("utf-8"))