from celery import shared_task
from django.utils.timezone import now
from django.core.cache import cache
from .models import ShortURL

@shared_task
def delete_expired_urls():
    """Deletes expired short URLs from the database and clears Redis cache"""
    expired_urls = ShortURL.objects.filter(expires_at__lt=now())
    
    # Remove expired URLs from Redis cache
    for url in expired_urls:
        cache.delete(url.short_code)

    expired_count, _ = expired_urls.delete()
    return f"Deleted {expired_count} expired short URLs"