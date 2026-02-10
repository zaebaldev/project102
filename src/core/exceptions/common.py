from .base import AppException

# === 4xx Client Errors ===


class NotFoundError(AppException):
    """Resource not found (404)."""

    message = "Resource not found"
    code = "NOT_FOUND"
    status_code = 404


class AlreadyExistsError(AppException):
    """Resource already exists (409)."""

    message = "Resource already exists"
    code = "ALREADY_EXISTS"
    status_code = 409


class ValidationError(AppException):
    """Validation error (422)."""

    message = "Validation error"
    code = "VALIDATION_ERROR"
    status_code = 422


class AuthenticationError(AppException):
    """Authentication failed (401)."""

    message = "Authentication failed"
    code = "AUTHENTICATION_ERROR"
    status_code = 401


class PermissionDeniedError(AppException):
    """Authorization failed - insufficient permissions (403)."""

    message = "Insufficient permissions"
    code = "PERMISSION_DENIED_ERROR"
    status_code = 403


class RateLimitError(AppException):
    """Rate limit exceeded (429)."""

    message = "Rate limit exceeded"
    code = "RATE_LIMIT_EXCEEDED"
    status_code = 429


class BadRequestError(AppException):
    """Bad request (400)."""

    message = "Bad request"
    code = "BAD_REQUEST"
    status_code = 400


# === 5xx Server Errors ===


class ExternalServiceError(AppException):
    """External service unavailable (503)."""

    message = "External service unavailable"
    code = "EXTERNAL_SERVICE_ERROR"
    status_code = 503


class DatabaseError(AppException):
    """Database error (500)."""

    message = "Database error"
    code = "DATABASE_ERROR"
    status_code = 500


class InternalError(AppException):
    """Internal server error (500)."""

    message = "Internal server error"
    code = "INTERNAL_ERROR"
    status_code = 500
