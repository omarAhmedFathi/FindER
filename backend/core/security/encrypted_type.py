from sqlalchemy.types import TypeDecorator, String
from core.security.encryption import encrypt_pii, decrypt_pii

class EncryptedString(TypeDecorator):
    """
    Transparently encrypts data before saving to DB and decrypts when reading.
    Ensures that if the database is dumped, PII remains secure.
    """
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return encrypt_pii(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return decrypt_pii(value)
        return value
