import os
from celery import Celery
from celery.schedules import crontab

# Set Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_expired_urls_every_minute': {
        'task': 'api.tasks.delete_expired_urls',
        'schedule': crontab(minute='*/5'),  # Run every minute
    },
}