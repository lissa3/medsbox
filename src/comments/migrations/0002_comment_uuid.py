# Generated by Django 4.2.1 on 2023-09-24 20:13

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
