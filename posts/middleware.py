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
