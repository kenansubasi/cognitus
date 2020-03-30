from celery import Celery


CELERY_BROKER_URL =  "redis://redis:6379",
CELERY_RESULT_BACKEND = "redis://redis:6379"

celery_app = Celery("algorithm", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery_app.task()
def debug_task():
    print("hello world")
