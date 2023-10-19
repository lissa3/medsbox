from django.test import TestCase
from django.urls import reverse

from src.accounts.tests.factories import (
    AdminSupUserFactory,
    StaffUserFactory,
    UserFactory,
)
from src.posts.tests.factories import PostFactory


class PostDeveloperTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.sup_user = AdminSupUserFactory()
        self.author = StaffUserFactory(username="sally")
        self.joe = UserFactory()

        self.post_1 = PostFactory.create(
            author=self.author,
            title_ru="Паралич Бэлла",
            content_ru="вирус герпеса, лечение преднизолоном,инфекциями",
            title_en="Bell's palsy",
            content_en="herpes virus, treatment,prednisone,infections",
            status=0,
        )

        self.post_2 = PostFactory(
            title_ru="Инфекция кожи",
            title_en="Skin infections",
            content_ru="Лечение чего-то там",
            content_en="Treatment",
            status=0,
        )
        self.post_3 = PostFactory(
            status=2,
            title_ru="Гипербиллирубинемия у новорождённых",
            content_ru="Фото терапия ",
            title_en="Newborns Hyperbilirubinemia",
            content_en="Photo therapy",
        )
        self.post_4 = PostFactory(
            status=1,
            title_ru="Гипербиллирубинемия у новорождённых",
            content_ru="Фото терапия ",
            title_en="Newborns Hyperbilirubinemia",
            content_en="Photo therapy",
        )
        self.post_5 = PostFactory(
            status=1,
            title_ru="Гипербиллирубинемия у новорождённых",
            content_ru="Фото терапия ",
            title_en="Newborns Hyperbilirubinemia",
            content_en="Photo therapy",
        )

    def test_perm_dev_page_user(self):
        """user not superuser can NOT get private page for drafts"""
        url = reverse("devs:dev_page")
        joe_user = UserFactory()
        self.client.force_login(joe_user)

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 403)

    def test_super_user_perm_dev_page(self):
        """superuser can get private page for drafts"""
        url = reverse("devs:dev_page")

        self.client.force_login(self.sup_user)

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_author_perm_soft_delete(self):
        """post author (staff) can get sort-delete post"""

        url = reverse("devs:soft_delete_post", kwargs={"uuid": self.post_1.uuid})

        self.client.force_login(self.author)

        resp = self.client.post(url, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_super_user_perm_soft_delete(self):
        """superuser can get sort-delete post"""

        url = reverse("devs:soft_delete_post", kwargs={"uuid": self.post_1.uuid})

        self.client.force_login(self.sup_user)

        resp = self.client.post(url, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_auth__user_no_perm_soft_delete(self):
        """user not author or superuser can NOT sort-delete post"""

        url = reverse("devs:soft_delete_post", kwargs={"uuid": self.post_1.uuid})

        self.client.force_login(self.joe)

        resp = self.client.post(url, follow=True)

        self.assertEqual(resp.status_code, 403)
