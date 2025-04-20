from django.core.validators import ValidationError
from rest_framework import status as statuses


class CustomException(ValidationError):
    __slots__ = ['data', 'status']

    def __init__(self, data, status=statuses.HTTP_400_BAD_REQUEST):
        super().__init__(message=data, code=status, )
        self.status = status
        self.data = data
