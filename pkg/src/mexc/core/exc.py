from typed_core.exceptions import (
  ApiError,
  AuthError,
  BadRequest,
  Error,
  LogicError,
  NetworkError,
  RateLimited,
  ValidationError,
)

UserError = LogicError

__all__ = [
  'ApiError',
  'AuthError',
  'BadRequest',
  'Error',
  'LogicError',
  'NetworkError',
  'RateLimited',
  'UserError',
  'ValidationError',
]
