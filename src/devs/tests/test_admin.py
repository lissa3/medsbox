from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings
from django.urls import reverse
from django_webtest import WebTest

from src.accounts.admin import User
from src.accounts.tests.factories import AdminSupUserFactory, StaffUserFactory
from src.posts.models.post_model import Post
from src.posts.tests.factories import PostFactory


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class TestAdminDevelopers(TestCase):
    def setUp(self):
        self.sup_user = AdminSupUserFactory()
        self.group = Group.objects.create(name="devs")
        codenames = [
            "add_post",
            "change_post",
            "view_post",
        ]
        permissions = Permission.objects.filter(
            content_type__app_label="posts", codename__in=codenames
        )
        for permission in permissions.all():
            self.group.permissions.add(permission)

        self.staff_author = StaffUserFactory(username="bob")
        self.staff_author.groups.add(self.group)

        self.post_sup_user = PostFactory.create(
            author=self.sup_user,
            title_en="Bell's palsy",
            content_en="infections",
            status=0,
        )
        self.post_staff = PostFactory.create(
            author=self.staff_author,
            title_en="Bell's palsy",
            content_en="infections",
            status=0,
        )
        self.client.force_login(self.staff_author)

    def test_staff_user_can_load_view(self):
        """auth staff user belongs to devs group"""
        dev_group = User.objects.filter(groups__name="devs")

        self.assertTrue(self.staff_author in dev_group)

    def test_staff_user_can_view_posts(self):
        """auth staff user can view list of own posts in admin"""
        url = reverse("admin:posts_post_changelist")

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
