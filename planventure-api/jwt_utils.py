from datetime import timedelta
from typing import Any, Dict, Optional

from flask_jwt_extended import decode_token, create_access_token, create_refresh_token
from flask_jwt_extended.exceptions import NoAuthorizationError


def create_jwt_access_token(
    identity: Any,
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a JWT access token for a user identity."""
    return create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=expires_delta,
    )


def create_jwt_refresh_token(
    identity: Any,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT refresh token for a user identity."""
    return create_refresh_token(identity=identity, expires_delta=expires_delta)


def decode_jwt_token(token: str, allow_expired: bool = False) -> Dict[str, Any]:
    """Decode a JWT token and validate its signature and claims."""
    return decode_token(token, allow_expired=allow_expired)


def validate_jwt_token(token: str, allow_expired: bool = False) -> bool:
    """Validate a JWT token by decoding it and confirming it is signed correctly."""
    try:
        decode_jwt_token(token, allow_expired=allow_expired)
        return True
    except NoAuthorizationError:
        return False
    except Exception:
        return False
