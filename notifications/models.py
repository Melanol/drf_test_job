from datetime import datetime, timedelta

from django.db import models
from timezone_field import TimeZoneField


class Notification(models.Model):
    send_time = models.DateTimeField(default=datetime.now())
    text = models.CharField(max_length=255, blank=True, default='')
    filter = models.CharField(max_length=255, blank=True, default='')
    stop_sending_time = models.DateTimeField(default=datetime.now() + timedelta(minutes=60))


class Client(models.Model):
    phone = models.IntegerField(blank=False, null=False, unique=True)
    operator_code = models.IntegerField(editable=False)
    tag = models.CharField(max_length=255, blank=True)
    timezone = TimeZoneField(default="Europe/Moscow")

    def save(self, *args, **kwargs):
        self.operator_code = int(str(self.phone)[1:4])
        super().save(*args, **kwargs)


class Message(models.Model):
    delivery_init_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(max_length=255)
    notification_id = models.IntegerField()
    client_id = models.IntegerField()
