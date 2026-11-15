import logging
import time
from celery import shared_task
from .models import Note

logger = logging.getLogger(__name__)

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def notify_note_created(note_id):
    note = Note.objects.filter(pk=note_id).first()
    if note is None:
        return
    time.sleep(3)  # Имитация медленной операции
    logger.warning("Внешний сервис уведомлён о заметке %s", note.pk)
