# Generated by Django 4.2.1 on 2023-09-30 19:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0003_comment_own_reply"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="body",
            field=models.CharField(max_length=2000),
        ),
    ]
