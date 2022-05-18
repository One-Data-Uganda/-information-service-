from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "worker", backend=settings.CELERY_BACKEND, broker=settings.CELERY_BROKER
)

celery_app.conf.task_routes = {"information.*": {"queue": "information"}}
celery_app.conf.task_serializer = "pickle"
celery_app.conf.result_serializer = "pickle"
celery_app.conf.accept_content = ["pickle", "json"]

celery_app.conf.timezone = "Africa/Kampala"
celery_app.conf["USE_TZ"] = True
celery_app.conf["TIME_ZONE"] = "Africa/Kampala"
celery_app.conf.enable_utc = False
