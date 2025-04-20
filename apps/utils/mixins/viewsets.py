from django.db import transaction
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from ..exceptions import CustomException
from apps.utils import decorators as global_decorators
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.mixins import UpdateModelMixin


class ViewSetMixin:

    class CacheListAndRetrieveMethodsMixin:
        @method_decorator(cache_page(45))
        def list(self,request,*args, **kwargs):
            return super().list(request,*args, **kwargs)
        @method_decorator(cache_page(45))
        def retrieve(self,request,*args, **kwargs):
            return super().retrieve(request,*args, **kwargs)


    class RequestBodyValidationAndAtomicTransactionMixin:

        def dispatch(self, request, *args, **kwargs):
            """
            Allow setting fields as required before calling views
            sets up atomic transaction on view
            """
            self.args = args
            self.kwargs = kwargs
            request = self.initialize_request(request, *args, **kwargs)
            self.request = request
            self.headers = self.default_response_headers  # deprecate?

            try:
                self.initial(request, *args, **kwargs)

                # Get the appropriate handler method
                if request.method.lower() in self.http_method_names:
                    handler = getattr(self, request.method.lower(),
                                      self.http_method_not_allowed)
                else:
                    handler = self.http_method_not_allowed
                if request.method.lower() in ["post", "patch", "put", "delete", "get"]:
                    errors = []
                    if request.method.lower() == 'get':
                        data = request.GET
                    else:
                        data = request.data
                    required_fields = self.get_required_fields()
                    if callable(required_fields):
                        errors = required_fields(data)
                    else:
                        errors = dict()
                        for field in required_fields:
                            if not data.get(field):
                                errors[field] = ["This field is required"]
                        if errors:
                            response = Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            with transaction.atomic():
                                response = handler(request, *args, **kwargs)
                else:
                    with transaction.atomic():
                        response = handler(request, *args, **kwargs)

            except Exception as exc:
                response = self.handle_exception(exc)

            self.response = self.finalize_response(request, response, *args, **kwargs)
            return self.response

    class RequiredFieldsMixin:
        """setup default value for Required Fields"""
        def get_required_fields(self):
            return []

    class PartialUpdateModelMixin(UpdateModelMixin):
        def update(self,request,*args,**kwargs):
            partial = kwargs.get('partial', False)
            if not partial:
                raise MethodNotAllowed(method = request.method)
            return super().update(request, *args, **kwargs)
    class AutoAddOwnerToRequestDataOnCreationAndUpdate:
        """set owner for objects in request data"""
        @global_decorators.ensure_request_data_is_mutable
        @global_decorators.ensure_owner_is_added_to_request_data
        def create(self, request, *args, **kwargs):
            return super().create(request, *args, **kwargs)

        @global_decorators.ensure_request_data_is_mutable
        @global_decorators.ensure_owner_is_added_to_request_data
        def update(self, request, *args, **kwargs):
            return super().update(request, *args, **kwargs)
