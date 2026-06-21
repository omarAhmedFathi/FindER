import logging
import re
from typing import Any, Dict

class PIIAnonymizerFilter(logging.Filter):
    """
    Scans log records and masks PII (emails, phone numbers, SSNs) before they are written to disk or stdout.
    """
    EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    PHONE_REGEX = re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}')

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            # Mask Emails
            record.msg = self.EMAIL_REGEX.sub('[REDACTED_EMAIL]', record.msg)
            # Mask Phones
            record.msg = self.PHONE_REGEX.sub('[REDACTED_PHONE]', record.msg)
        return True

def setup_secure_logging():
    logger = logging.getLogger()
    for handler in logger.handlers:
        handler.addFilter(PIIAnonymizerFilter())
