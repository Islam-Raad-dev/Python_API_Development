from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError


class SecurityManager:
    """
    Production-grade Password Hashing Architecture.
    Uses Argon2id with memory-hard parameters to mitigate GPU/ASIC attacks.
    """

    def __init__(self):
        self._ph = PasswordHasher(
            time_cost=3,  # 3 Iterations
            memory_cost=65536,  # 64 MB RAM per operation
            parallelism=4,  # 4 Parallel Threads
            hash_len=32,
            salt_len=16,  # Automatic secure random salt generation
        )

    def hash_password(self, password: str) -> str:
        if not password or len(password) < 8:
            raise ValueError("Password does not meet minimum length requirements.")
        return self._ph.hash(password)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        try:
            return self._ph.verify(hashed_password, password)
        except (VerifyMismatchError, InvalidHashError, VerificationError):
            return False

    def check_and_rehash(self, hashed_password: str, password: str):
        """Verifies password and returns a new hash if parameters were upgraded."""
        if self.verify_password(hashed_password, password):
            if self._ph.check_needs_rehash(hashed_password):
                return True, self.hash_password(password)
            return True, None
        return False, None
