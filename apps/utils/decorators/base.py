import typing

from django.http import QueryDict


def ensure_request_data_is_mutable(function):
    def function_to_execute(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        return function(self, request, *args, **kwargs)

    function_to_execute.__name__ = function.__name__
    return function_to_execute

def ensure_owner_is_added_to_request_data(function):
    def function_to_execute(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            for obj in request.data:
                obj['owner'] = request.user.id
        else:
            request.data['owner'] = request.user.id
        return function(self, request, *args, **kwargs)

    function_to_execute.__name__ = function.__name__
    return function_to_execute

