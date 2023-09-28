# Generated by Django 4.2.1 on 2023-09-24 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0002_comment_uuid"),
        ("posts", "0005_add_unique"),
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={"ordering": ["-created"]},
        ),
        migrations.AddField(
            model_name="notification",
            name="parent_comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="comments.comment",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="posts.post",
            ),
        ),
    ]