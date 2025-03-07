from django.urls import path
from .views import shorten_url, retrieve_url, redirect_to_original, get_url_stats

urlpatterns = [
    path('shorten/', shorten_url, name='shorten_url'),
    path('retrieve/', retrieve_url, name='retrieve_url'),
    path('<str:short_code>/', redirect_to_original, name='redirect_to_original'),
    path('stats/<str:short_code>/', get_url_stats, name='get_url_stats'),
]
