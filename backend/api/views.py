from django.core.cache import cache  # Import cache
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ShortURL
from .serializers import ShortURLSerializer

@api_view(['POST'])
def shorten_url(request):
    """Creates a new short URL every time and ensures expired links are deleted"""
    long_url = request.data.get("long_url")

    if not long_url:
        return Response({"error": "long_url field is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Delete expired URLs before creating a new one
    ShortURL.objects.filter(expires_at__lt=now()).delete()

    # Validate the URL
    serializer = ShortURLSerializer(data={"original_url": long_url})
    if serializer.is_valid():
        # Always create a new short URL
        url_obj = ShortURL.objects.create(original_url=serializer.validated_data["original_url"])
        return Response({
            "short_url": url_obj.short_code,
            "expires_at": url_obj.expires_at.strftime('%Y-%m-%d %H:%M:%S')  # Return expiration info
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_url(request):
    """Retrieves the original URL from a short code"""
    short_code = request.GET.get("short_url")
    url_obj = get_object_or_404(ShortURL, short_code=short_code)

    url_obj.visit_count += 1
    url_obj.save()

    return Response({"long_url": url_obj.original_url}, status=status.HTTP_200_OK)

@api_view(['GET'])
def redirect_to_original(request, short_code):
    """Redirects short URL to the original URL with caching"""

    # Check Redis cache first
    cached_url = cache.get(short_code)
    if cached_url:
        return redirect(cached_url)  # Instant redirect from Redis cache

    # If not in cache, query the database
    url_obj = get_object_or_404(ShortURL, short_code=short_code)

    # Prevent redirecting if URL has expired
    if url_obj.expires_at and url_obj.expires_at < now():
        return Response({"error": "This short URL has expired."}, status=status.HTTP_410_GONE)

    # Store in Redis cache for faster access
    cache.set(short_code, url_obj.original_url, timeout=600)  # Cache for 10 min

    url_obj.visit_count += 1
    url_obj.save()
    return redirect(url_obj.original_url)

@api_view(['GET'])
def get_url_stats(request, short_code):
    """Returns access statistics for a short URL"""
    url_obj = get_object_or_404(ShortURL, short_code=short_code)
    return Response({
        "original_url": url_obj.original_url,
        "short_code": url_obj.short_code,
        "visit_count": url_obj.visit_count
    }, status=status.HTTP_200_OK)
