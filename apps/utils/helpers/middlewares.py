from django.http import HttpResponseNotAllowed


class BlockPutRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "PUT":
            return HttpResponseNotAllowed(permitted_methods=['GET', 'POST', 'DELETE'])
        response = self.get_response(request)
        return response
