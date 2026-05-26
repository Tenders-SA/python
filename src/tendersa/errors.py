from __future__ import annotations


class TendersaError(Exception):
    """Base exception for all Tenders-SA API errors."""

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        request_id: str = "",
        docs: str = "",
    ) -> None:
        self.status = status
        self.code = code
        self.request_id = request_id
        self.docs = docs
        super().__init__(message)


class BadRequestError(TendersaError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(400, "BAD_REQUEST", message, request_id)


class AuthError(TendersaError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(401, "UNAUTHORIZED", message, request_id)


class ForbiddenError(TendersaError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(403, "FORBIDDEN", message, request_id)


class NotFoundError(TendersaError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(404, "NOT_FOUND", message, request_id)


class ConflictError(TendersaError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(409, "CONFLICT", message, request_id)


class RateLimitError(TendersaError):
    def __init__(
        self,
        message: str,
        request_id: str = "",
        limit: int = 0,
        used: int = 0,
        resets_at: str = "",
        tier: str = "",
    ) -> None:
        super().__init__(429, "RATE_LIMIT_EXCEEDED", message, request_id)
        self.limit = limit
        self.used = used
        self.resets_at = resets_at
        self.tier = tier


class InternalError(TendersaError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(500, "INTERNAL_ERROR", message, request_id)


class ServiceUnavailableError(TendersaError):
    def __init__(self, message: str, request_id: str = "") -> None:
        super().__init__(502, "SERVICE_UNAVAILABLE", message, request_id)


_STATUS_ERROR_MAP: dict[int, type[TendersaError]] = {
    400: BadRequestError,
    401: AuthError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    429: RateLimitError,
    500: InternalError,
    502: ServiceUnavailableError,
}


def create_error_from_response(
    status: int,
    error: str = "",
    code: str = "",
    message: str = "",
    request_id: str = "",
    details: dict | None = None,
) -> TendersaError:
    err_cls = _STATUS_ERROR_MAP.get(status, TendersaError)
    msg = message or error or "Unknown error"
    code_val = code or err_cls.__name__.upper().replace("ERROR", "")

    if err_cls is TendersaError:
        return TendersaError(status, code_val, msg, request_id)

    if status == 429:
        d = details or {}
        return RateLimitError(
            msg, request_id,
            limit=d.get("limit", 0),
            used=d.get("used", 0),
            resets_at=d.get("resetsAt", ""),
            tier=d.get("tier", ""),
        )

    return err_cls(msg, request_id)
