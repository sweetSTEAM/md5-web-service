from celery import shared_task
from .md5core import get_md5

@shared_task(bind=True, track_started=True)
def get_md5_task(self, url):
    return get_md5(self, url)

