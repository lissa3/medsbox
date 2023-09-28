from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from src.accounts.tests.factories import UserFactory
from src.comments.models import Comment
from src.contacts.exceptions import HtmxFailureError
from src.notifications.models import Notification
from src.posts.tests.factories import PostFactory


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class NotificationsFabricTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = UserFactory(username="tata")
        self.author_comment = UserFactory(username="sally")
        self.post = PostFactory.create(
            title_en="Bell's palsy",
            content_en="herpes virus, treatment,prednisone",
            status=2,
        )
        self.comment = Comment.add_root(
            post=self.post, user=self.author_comment, body="it's me, root comment"
        )

    def test_notific_on_reply_comment(self):
        """test adding child comment(reply to a root comment)"""
        self.client.force_login(self.user)
        url = reverse(
            "comments:process_comm",
            kwargs={"post_uuid": self.post.uuid},
        )
        data = {
            "body": "Tata replies Sally",
            "comm_parent_id": self.comment.id,
            "post": self.post,
        }
        headers = {"HTTP_HX-Request": "true"}

        resp = self.client.post(url, data=data, **headers)

        notif_count = Notification.objects.count()
        notif_to_author = Notification.objects.last()

        self.assertEqual(resp.status_code, 204)
        self.assertFalse(notif_to_author.read)
        self.assertEqual(notif_to_author.post, self.post)
        self.assertEqual(notif_to_author.parent_comment, self.comment)
        self.assertEqual(notif_to_author.recipient, self.author_comment)
        self.assertEqual(notif_count, 1)


def test_no_notif_own_reply_to_yourself(self):
    """if user reply's own comment -> no notifications"""
    self.client.force_login(self.author_comment)
    url = reverse(
        "comments:process_comm",
        kwargs={"post_uuid": self.post.uuid},
    )
    data = {
        "body": "Sally reply's to herself",
        "comm_parent_id": self.comment.id,
        "post": self.post,
    }
    headers = {"HTTP_HX-Request": "true"}

    resp = self.client.post(url, data=data, **headers)

    notif_count = Notification.objects.count()

    self.assertEqual(resp.status_code, 204)
    self.assertEqual(notif_count, 0)


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class MarkNotificationsAsReadTestCase(TestCase):
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

    def test_mark_notific_as_read(self):
        """mark all notifications as read"""
        self.client.force_login(self.user)
        url = reverse(
            "notifications:mark_top_read",
        )
        headers = {"HTTP_HX-Request": "true", "HTTP_REFERER": "foo"}

        resp = self.client.post(url, **headers)

        notifs = Notification.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(notifs[0].read)
        self.assertTrue(notifs[1].read)

    def test_failure_notific_as_read(self):
        """fail to mark all notifications as read"""
        self.client.force_login(self.user)
        url = reverse(
            "notifications:mark_top_read",
        )
        print("I am here")
        with self.assertRaises(HtmxFailureError) as e:
            resp = self.client.post(url)  # noqa

        self.assertEqual(str(e.exception), _("Something went wrong.Please try later"))
