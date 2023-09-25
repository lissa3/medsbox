from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_webtest import WebTest

from src.accounts.tests.factories import UserFactory
from src.comments.models import Comment
from src.notifications.models import Notification
from src.posts.tests.factories import PostFactory

User = get_user_model()


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class NotificationsActionsTestCase(WebTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = UserFactory(username="tata")
        self.author_comment = UserFactory(username="sally")
        self.post = PostFactory.create(
            title_en="Bell's palsy",
            content_en="herpes virus, treatment,prednisone",
            status=2,
        )
        self.root_comment = Comment.add_root(
            post=self.post, user=self.author_comment, body="it's me, root comment"
        )
        self.notif_1 = Notification.objects.create(
            recipient=self.user, parent_comment=self.root_comment, post=self.post
        )
        self.notif_2 = Notification.objects.create(
            recipient=self.user, parent_comment=self.root_comment, post=self.post
        )

    def test_notific_on_reply_comment(self):
        """div notifications in dropdown exists"""

        self.app.set_user(self.user)
        url = reverse("home")

        resp = self.app.get(url)

        dropdow_notifications = resp.html.find("div", id="notis")

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(dropdow_notifications)
