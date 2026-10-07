import bcrypt
def hash_password(plain: str) -> str:
    pw_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed.decode("utf-8")