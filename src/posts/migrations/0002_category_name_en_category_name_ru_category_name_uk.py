# Generated by Django 4.2.1 on 2023-07-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="name_en",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="name_ru",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="name_uk",
            field=models.CharField(max_length=30, null=True),
        ),
    ]