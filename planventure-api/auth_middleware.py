from functools import wraps
from typing import Any, Callable, Optional

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request

from models import User


def get_current_user() -> Optional[User]:
    """Get the current authenticated user from JWT token.

    Returns:
        User instance if authenticated, None otherwise
    """
    try:
        verify_jwt_in_request()
        user_id_str = get_jwt_identity()
        if user_id_str:
            user_id = int(user_id_str)
            return User.query.get(user_id)
    except Exception:
        pass
    return None


def require_auth(f: Callable) -> Callable:
    """Decorator to require JWT authentication on a route.

    Args:
        f: The route function to decorate

    Returns:
        Decorated function that requires authentication
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # JWT verification is handled by @jwt_required()
        # Additional user validation can be added here if needed
        return f(*args, **kwargs)
    return decorated_function


def require_user(f: Callable) -> Callable:
    """Decorator to require JWT authentication and provide current user.

    This decorator ensures the user is authenticated and injects the
    current user as the first argument after 'self' (if it's a method).

    Args:
        f: The route function to decorate

    Returns:
        Decorated function with current user injected
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found.'}), 404

        # Inject user as first argument (after self if it's a method)
        return f(user, *args, **kwargs)
    return decorated_function


def optional_auth(f: Callable) -> Callable:
    """Decorator for optional JWT authentication.

    The route can work with or without authentication.
    Use get_current_user() inside the route to check if user is authenticated.

    Args:
        f: The route function to decorate

    Returns:
        Decorated function with optional authentication
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # Try to verify JWT but don't fail if it's missing/invalid
        try:
            verify_jwt_in_request()
        except Exception:
            pass  # Authentication is optional

        return f(*args, **kwargs)
    return decorated_function


def admin_required(f: Callable) -> Callable:
    """Decorator to require admin privileges.

    This is a placeholder for future admin role implementation.
    Currently just requires authentication.

    Args:
        f: The route function to decorate

    Returns:
        Decorated function requiring admin access
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found.'}), 404

        # TODO: Add admin role check when roles are implemented
        # if not user.is_admin:
        #     return jsonify({'error': 'Admin access required.'}), 403

        return f(*args, **kwargs)
    return decorated_function


# Convenience function for manual token verification
def verify_request_auth() -> tuple[bool, Optional[User]]:
    """Manually verify JWT authentication in request.

    Returns:
        Tuple of (is_authenticated: bool, user: User or None)
    """
    try:
        verify_jwt_in_request()
        user_id_str = get_jwt_identity()
        if user_id_str:
            user_id = int(user_id_str)
            user = User.query.get(user_id)
            return True, user
    except Exception:
        pass
    return False, None