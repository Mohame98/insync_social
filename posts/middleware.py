from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.utils.deprecation import MiddlewareMixin
from django.db.models.query import QuerySet

class RateLimitMiddleware(MiddlewareMixin):
    @method_decorator(ratelimit(key='ip', rate='5/m', method='ALL', block=False)) 
    def process_request(self, request):
        if getattr(request, 'limited', False):
            return JsonResponse({'error': 'Too many requests'}, status=429)


original_queryset_init = QuerySet.__init__

def queryset_init_with_limit(self, *args, **kwargs):
    original_queryset_init(self, *args, **kwargs)
    if not getattr(self, '_limit_applied', False) and not any(x in str(self.query) for x in ['django_session', 'auth_permission']):
        self._limit_applied = True
        self.query.set_limits(high=500)


QuerySet.__init__ = queryset_init_with_limit

class QueryLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response        