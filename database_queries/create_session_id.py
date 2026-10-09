import string
from sqlalchemy import text
from Engine import engine
CHARACTERS = string.ascii_letters + string.digits
BASE = len(CHARACTERS)
def encode_session_id(number: int) -> str:
    if not 1 <= number <= 2_000_000_000:
        raise ValueError("Session ID number is out of range")
    result = []
    for _ in range(10):
        result.append(CHARACTERS[number % BASE])
        number //= BASE
    if number:
        raise OverflowError("Session ID exceeds 10 characters")
    return "".join(result)
def create_session_id() -> str:
    with engine.connect() as connection:
        number = connection.execute(text("SELECT nextval('session_id_sequence')")).scalar_one()
    return encode_session_id(number)