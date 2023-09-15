import json

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from src.accounts.tests.factories import UserFactory
from src.comments.models import Comment
from src.posts.tests.factories import PostFactory

User = get_user_model()


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class HtmxCommentsFunctionsViewsTestCase(TestCase):
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
            post=self.post, user=self.author_comment, body="it's me root comment"
        )

    def test_get_reply_form(self):
        """ """
        user = UserFactory()
        self.client.force_login(user)

        url = reverse(
            "comments:add_comm",
            kwargs={"post_id": self.post.id, "comm_id": self.comment.id},
        )
        headers = {"HTTP_HX-Request": "true"}
        resp = self.client.get(url, **headers)
        form = resp.context["form"]

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(form.is_bound)
        self.assertTrue(form.initial, {"comm_parent_id": str(self.comment.id)})

    def test_post_reply_comment(self):
        """test adding child comment(reply to a root comment)"""
        start_comments = Comment.objects.all()
        count_start = start_comments.count()
        user = UserFactory()
        self.client.force_login(user)
        url = reverse(
            "comments:process_comm",
            kwargs={"post_id": self.post.id},
        )
        data = {"body": "reply to a root comment", "comm_parent_id": self.comment.id}
        headers = {"HTTP_HX-Request": "true"}
        resp = self.client.post(url, data=data, **headers)

        self.comment.refresh_from_db()

        final_comments = Comment.objects.all()
        parent = final_comments.first()

        kids = parent.get_children_count()
        kid = parent.get_children()[0]

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(count_start, 1)
        self.assertEqual(final_comments.count(), 2)
        self.assertEqual(kids, 1)
        self.assertEqual(kid.reply_to, self.author_comment)

    def test_auth_comment_tools(self):
        """comment author has links to fetch a form for edit and delete"""

        self.client.force_login(self.author_comment)
        url = reverse("comments:all_comms", kwargs={"post_id": self.post.id})
        headers = {"HTTP_HX-Request": "true"}
        resp = self.client.get(url, **headers)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'hx-target="#dialog"')
        self.assertContains(resp, 'hx-get="/en/comments/edit-comm')
        self.assertContains(resp, 'hx-get="/en/comments/process-delete')

    def test_auth_user_no_comment_tools(self):
        """auth user not comment author has No links for edit and delete"""

        self.client.force_login(self.user)
        url = reverse("comments:all_comms", kwargs={"post_id": self.post.id})
        headers = {"HTTP_HX-Request": "true"}
        resp = self.client.get(url, **headers)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'hx-target="#dialog"')
        self.assertNotContains(resp, 'hx-get="/en/comments/edit-comm')
        self.assertNotContains(resp, 'hx-get="/en/comments/process-delete')

    def test_anonymous_no_reply_no_comment_tools(self):
        """not auth user has no link to reply or edit/delete cooment"""

        url = reverse("comments:all_comms", kwargs={"post_id": self.post.id})
        headers = {"HTTP_HX-Request": "true"}
        resp = self.client.get(url, **headers)

        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'hx-target="#dialog"')
        self.assertNotContains(resp, 'hx-get="/en/comments/edit-comm')
        self.assertNotContains(resp, 'hx-get="/en/comments/process-delete')
