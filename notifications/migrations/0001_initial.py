# Generated by Django 4.2.1 on 2023-05-31 15:46

import datetime
from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.IntegerField(unique=True)),
                ("operator_code", models.IntegerField(editable=False)),
                ("tag", models.CharField(blank=True, max_length=255)),
                (
                    "timezone",
                    timezone_field.fields.TimeZoneField(default="Europe/Moscow"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("delivery_init_time", models.DateTimeField(blank=True, null=True)),
                ("delivered_time", models.DateTimeField(blank=True, null=True)),
                ("delivery_status", models.CharField(max_length=255)),
                ("notification_id", models.IntegerField()),
                ("client_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "send_time",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 5, 31, 15, 46, 18, 999295)
                    ),
                ),
                ("text", models.CharField(blank=True, default="", max_length=255)),
                ("filter", models.CharField(blank=True, default="", max_length=255)),
                (
                    "stop_sending_time",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 5, 31, 16, 46, 18, 999371)
                    ),
                ),
            ],
        ),
    ]
