from django.urls import reverse, reverse_lazy
from django_webtest import WebTest

from src.accounts.tests.factories import AdminSupUserFactory
from src.posts.tests.factories import PostFactory


class MyTestCase(WebTest):
    def setUp(self):
        super().setUp()
        self.user = AdminSupUserFactory.create()
        self.client.force_login(self.user)
        self.post = PostFactory.create(
            author=self.user,
            title_ru="Паралич Бэлла",
            content_ru="вирус герпеса, лечение преднизолоном,инфекциями",
            title_en="Bell's palsy",
            content_en="herpes virus, treatment,prednisone,infections",
            status=0,
        )
        self.post_2 = PostFactory(
            status=1,
            title_ru="Гипербиллирубинемия у новорождённых",
            content_ru="Фото терапия ",
            title_en="Newborns Hyperbilirubinemia",
            content_en="Photo therapy",
        )

    def test_choices_buttons_dashboard(self):
        """buttons for diff actions should be present on dev detail post"""
        self.app.set_user(self.user)
        url = reverse("devs:dev_page")

        response = self.app.get(url)

        response.mustcontain("Show drafts", "Show reviews", "Show soft-deleted")
        menu_buttons = response.html.findAll("div", "menu_item")

        assert response.status_code == 200
        assert len(menu_buttons) == 3

    def test_dev_to_review(self):
        """check form submission: post status draft -> review"""
        self.app.set_user(self.user)
        url = reverse("devs:dev_detail_post", kwargs={"uuid": self.post.uuid})

        resp_detail = self.app.get(url)

        assert resp_detail.status_code == 200

        form = resp_detail.forms["toReview"]
        resp_change = form.submit().follow()

        self.post.refresh_from_db()
        assert resp_change.status_code == 200
        assert self.post.status == 1

    def test_dev_to_public(self):
        """inspect html form: status review -> public"""
        self.app.set_user(self.user)
        url = reverse("devs:dev_detail_post", kwargs={"uuid": self.post_2.uuid})

        resp_detail = self.app.get(url)
        assert resp_detail.status_code == 200

        form = resp_detail.html.find("form", id="toPublic")

        assert form.attrs["method"] == "POST"
