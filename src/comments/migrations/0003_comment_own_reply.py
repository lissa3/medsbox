# Generated by Django 4.2.1 on 2023-09-25 08:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0002_comment_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="own_reply",
            field=models.BooleanField(default=False),
        ),
    ]
