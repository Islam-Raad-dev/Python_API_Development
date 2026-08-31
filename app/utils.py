from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,  # 64MB RAM
    parallelism=4,
    hash_len=32,
    salt_len=16,
)

def hash_password(password: str) -> str:
        if not password or len(password) < 8:
            raise ValueError("Password does not meet minimum length requirements.")
        return ph.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
        try:
            return ph.verify(hashed_password, password)
        except (VerifyMismatchError, InvalidHashError, VerificationError):
            return False

def check_and_rehash(hashed_password: str, password: str):
        """Verifies password and returns a new hash if parameters were upgraded."""
        if verify_password(hashed_password, password):
            if ph.check_needs_rehash(hashed_password):
                return True, hash_password(password)
            return True, None
        return False, None
