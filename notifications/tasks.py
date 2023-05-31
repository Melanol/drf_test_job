# The tasks are outside of Django. Hence, we need to do some imports
# https://stackoverflow.com/questions/26082128/improperlyconfigured-you-must-either-define-the-environment-variable-django-set
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_test_job.settings")
import django
django.setup()
from django.core.management import call_command


import requests

from celery import Celery
from django.http import HttpResponse
from django.conf import settings


app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y):
    return x + y


@app.task
def notify(notification_id, client_id, phone, text):
    from notifications.models import Message
    message = Message(notification_id=notification_id, client_id=client_id)
    message.save()  # TODO: Message.delivered
    request_body = {
        "id": message.id,
        "phone": phone,
        "text": text
    }
    response = requests.post(f"https://probe.fbrq.cloud/v1/send/{message.id}",
                             headers={"Authorization": f"Bearer {settings.TOKEN}"},
                             json=request_body)
    return response.json()
