import os
from logging import warning

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dear_diary_django.settings')

app = Celery('diary_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_old_diaries': {
        'task': 'diary_app.tasks.delete_old_diaries',
        'schedule': 600,
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    warning(f'Request: {self.request!r}')

