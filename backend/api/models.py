from django.db import models
import string
import random
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
# Create your models here.


class ShortURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True) # Expiration date for the short URL
    visit_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=10) # Default expiration time is 10 minutes
        super().save(*args, **kwargs)

    def generate_short_code(self, length=6):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=length))
            if not ShortURL.objects.filter(short_code=short_code).exists():
                return short_code

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
