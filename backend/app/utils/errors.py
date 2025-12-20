class APIError(Exception):
    def __init__(self, code, message, status_code=400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)

class ValidationError(APIError):
    def __init__(self, message, details=None):
        super().__init__('validation_error', message, 400, details)

class AuthenticationError(APIError):
    def __init__(self, message='Authentication failed'):
        super().__init__('unauthorized', message, 401)

class NotFoundError(APIError):
    def __init__(self, resource='Resource'):
        super().__init__('not_found', f'{resource} not found', 404)

class ConflictError(APIError):
    def __init__(self, message='Resource already exists'):
        super().__init__('conflict', message, 409)
