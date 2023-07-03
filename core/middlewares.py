from django.utils.deprecation import MiddlewareMixin

class RequestCounterMiddleware(MiddlewareMixin):
    request_count = 0

    def process_request(self, request):
        RequestCounterMiddleware.request_count += 1
