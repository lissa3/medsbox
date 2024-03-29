# Generated by Django 4.2.1 on 2023-08-22 19:51
from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector_ru(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    vector_ru = SearchVector("title_ru", weight="A", config="russian") + SearchVector(
        "content_ru", weight="B", config="russian"
    )

    Post.objects.update(vector_ru=vector_ru)


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_post_vector_en_post_vector_ru_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER vector_ru_trigger
            BEFORE INSERT OR UPDATE OF title_ru, content_ru, vector_ru
            ON posts_post
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                vector_ru, 'pg_catalog.russian', title_ru, content_ru
            );
            UPDATE posts_post SET vector_ru = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS vector_ru_trigger
            ON posts_post;
            """,
        ),
        migrations.RunPython(
            compute_search_vector_ru, reverse_code=migrations.RunPython.noop
        ),
    ]
