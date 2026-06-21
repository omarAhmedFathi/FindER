from cryptography.fernet import Fernet
import os
import logging

logger = logging.getLogger("security")

# In production, this key MUST be injected via environment variables
ENCRYPTION_KEY = os.getenv("FERNET_ENCRYPTION_KEY", Fernet.generate_key().decode())
fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_pii(data: str) -> str:
    """Encrypts Personally Identifiable Information (PII) using AES-256."""
    if not data:
        return data
    try:
        return fernet.encrypt(data.encode()).decode()
    except Exception as e:
        logger.error(f"Encryption failure: {str(e)}")
        raise ValueError("Failed to encrypt PII data")

def decrypt_pii(encrypted_data: str) -> str:
    """Decrypts PII back to plaintext."""
    if not encrypted_data:
        return encrypted_data
    try:
        return fernet.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        logger.error(f"Decryption failure: {str(e)}")
        raise ValueError("Failed to decrypt PII data")
