from celery import shared_task
import time
from django.conf import settings
import redis

r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True)

@shared_task
def wait_and_delete_status(redis_order_id):
    time.sleep(3600)
    r.delete(redis_order_id)