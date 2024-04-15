from celery import shared_task

from django.utils import timezone

from .models import Diary



@shared_task
def delete_old_diaries():
    current_time = timezone.now()
    diaries_to_delete = Diary.objects.filter(expiration__lt=current_time)
    diaries_to_delete.delete()
