"""Custom exception classes for GeoAir application"""


class GeoAirException(Exception):
    """Base exception for GeoAir application"""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NewsAPIError(GeoAirException):
    """Exception raised when News API request fails"""
    
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message, status_code)


class DatabaseError(GeoAirException):
    """Exception raised when database operation fails"""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class ValidationError(GeoAirException):
    """Exception raised when validation fails"""
    
    def __init__(self, message: str, status_code: int = 422):
        super().__init__(message, status_code)


class ResourceNotFoundError(GeoAirException):
    """Exception raised when requested resource is not found"""
    
    def __init__(self, message: str, resource_type: str = "Resource"):
        super().__init__(f"{resource_type} not found: {message}", 404)
