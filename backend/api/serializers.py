from rest_framework import serializers
from .models import ShortURL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_code', 'visit_count']
        
        def validate_original_url(self, value):
            """Validates the original URL"""
            validator = URLValidator()
            try:
                validator(value)
            except ValidationError:
                raise serializers.ValidationError("Invalid URL format. Please enter a valid URL.")
            
            # Ensure the URL starts with http:// or https://
            if not value.startswith(("http://", "https://")):
                raise serializers.ValidationError("Invalid URL format. Please enter a valid URL.")
            
            return value