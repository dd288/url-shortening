from django.core.cache import cache
from django.http import JsonResponse

class BlockSpammingIPs:
    """Middleware to block repeated IPs that exceed rate limits"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        blocked_ips = cache.get('blocked_ips', [])

        if ip in blocked_ips:
            return JsonResponse({"error": "Your IP has been temporarily blocked due to excessive requests."}, status=403)

        response = self.get_response(request)

        if response.status_code == 429:  # If throttling is triggered
            attempt_count = cache.get(ip, 0) + 1
            cache.set(ip, attempt_count, timeout=600)  # Track failed attempts for 10 min
            if attempt_count >= 5:  # If exceeded limit multiple times
                blocked_ips.append(ip)
                cache.set('blocked_ips', blocked_ips, timeout=600)  # Block for 10 minutes
                return JsonResponse({"error": "Your IP has been blocked for 10 minutes due to excessive requests."}, status=403)

        return response
