from .celery import app as celery_app

# Django가 시작할 때 shared_task가 이 앱을 이용할 수 있도록
# app이 항상 import

__all__ = ('celery_app',)
