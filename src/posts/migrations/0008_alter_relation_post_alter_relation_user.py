# Generated by Django 4.2.1 on 2023-10-26 16:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0007_like_func"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relation",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post_rel",
                to="posts.post",
            ),
        ),
        migrations.AlterField(
            model_name="relation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_rel",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]