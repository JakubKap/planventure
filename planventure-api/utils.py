import hashlib
import os
from typing import Tuple

from werkzeug.security import check_password_hash, generate_password_hash


def generate_salt(length: int = 32) -> str:
    """Generate a random salt for password hashing.

    Args:
        length: Length of the salt in bytes (default: 32)

    Returns:
        Hexadecimal string representation of the salt
    """
    return os.urandom(length).hex()


def hash_password_with_salt(password: str, salt: str = None) -> Tuple[str, str]:
    """Hash a password with a salt using PBKDF2.

    Args:
        password: The plain text password to hash
        salt: Optional salt to use. If None, generates a new salt.

    Returns:
        Tuple of (hashed_password, salt_used)
    """
    if salt is None:
        salt = generate_salt()

    # Use PBKDF2 with SHA-256, 100,000 iterations
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()

    return hashed, salt


def verify_password_with_salt(password: str, hashed_password: str, salt: str) -> bool:
    """Verify a password against a hash and salt.

    Args:
        password: The plain text password to verify
        hashed_password: The stored hash
        salt: The salt used for hashing

    Returns:
        True if password matches, False otherwise
    """
    expected_hash, _ = hash_password_with_salt(password, salt)
    return expected_hash == hashed_password


def hash_password_werkzeug(password: str) -> str:
    """Hash a password using Werkzeug's generate_password_hash (includes salt).

    Args:
        password: The plain text password to hash

    Returns:
        Hashed password string with salt included
    """
    return generate_password_hash(password)


def verify_password_werkzeug(password: str, hashed_password: str) -> bool:
    """Verify a password using Werkzeug's check_password_hash.

    Args:
        password: The plain text password to verify
        hashed_password: The stored hashed password

    Returns:
        True if password matches, False otherwise
    """
    return check_password_hash(hashed_password, password)


# Convenience functions for common use cases
def create_password_hash(password: str, method: str = 'werkzeug') -> str:
    """Create a password hash using the specified method.

    Args:
        password: The plain text password
        method: 'werkzeug' (default) or 'pbkdf2'

    Returns:
        Hashed password string
    """
    if method == 'pbkdf2':
        hashed, salt = hash_password_with_salt(password)
        return f"pbkdf2:{salt}:{hashed}"
    else:
        return f"werkzeug:{hash_password_werkzeug(password)}"


def verify_password_hash(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash with method prefix.

    Args:
        password: The plain text password
        stored_hash: The stored hash with method prefix (e.g., 'werkzeug:hash' or 'pbkdf2:salt:hash')

    Returns:
        True if password matches, False otherwise
    """
    try:
        if stored_hash.startswith('pbkdf2:'):
            # Custom PBKDF2 format: pbkdf2:salt:hash
            _, salt, hashed = stored_hash.split(':', 2)
            return verify_password_with_salt(password, hashed, salt)
        elif stored_hash.startswith('werkzeug:'):
            # Werkzeug format: werkzeug:hash
            _, werkzeug_hash = stored_hash.split(':', 1)
            return verify_password_werkzeug(password, werkzeug_hash)
        else:
            # Assume it's a plain werkzeug hash (backward compatibility)
            return verify_password_werkzeug(password, stored_hash)
    except Exception:
        return False