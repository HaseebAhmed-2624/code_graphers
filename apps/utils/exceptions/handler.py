from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import exception_handler
# from stripe import _error as err


from . import CustomException
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    if isinstance(exc, CustomException):
        response = Response({"message": exc.data}, status=exc.status, )
    elif isinstance(exc, AuthenticationFailed):
        response = Response({"message": exc.args[0]}, status=exc.status_code)
    elif isinstance(exc, Http404):
        response = Response({"message": str(exc)}, status=status.HTTP_404_NOT_FOUND)
    else:
        response = exception_handler(exc, context)
    return response

