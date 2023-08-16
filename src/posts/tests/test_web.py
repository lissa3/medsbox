from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest
from taggit.models import Tag
from webtest import TestApp

from src.accounts.tests.factories import AdminSupUserFactory
from src.contacts.models import NewsLetter
from src.contacts.tests.factories import NewsLetterFactory
from src.core.utils.admin_help import admin_change_url
from src.posts.models.post_model import Post
from src.posts.tests.factories import PostFactory

User = get_user_model()
TestApp.__test__ = False


class TestAdminPostForm(WebTest):
    def setUp(self):
        super().setUp()
        self.user = AdminSupUserFactory()
        self.app.set_user(self.user)
        self.letter = NewsLetterFactory(letter_status=1)
        self.letter = NewsLetterFactory(letter_status=1)

    def test_admin_create_post(self):
        """
        initial post form has per-filled fields:
        author(current user) and letters(status to be send);
        select field has default
        [('', False, '----'), ('1', True, 'Letter #id 1'),..]
        """
        get_form_url = reverse("admin:posts_post_add")
        resp_initial = self.app.get(get_form_url)

        self.assertEqual(resp_initial.status_code, 200)

        initial_form = resp_initial.forms["post_form"]

        last_letter = NewsLetter.objects.last()
        author_value = int(initial_form["author"].value)
        letter_value = int(initial_form["letter"].value)

        letter_options = initial_form["letter"].options

        self.assertEqual(author_value, self.user.id)
        self.assertEqual(letter_value, last_letter.id)
        self.assertEqual(len(letter_options), 3)
        self.assertEqual(letter_options[0][1], False)

    def test_admin_post_list_link_to_category(self):
        """
        post list contains a link to a category obj
        ex: # /admin/posts/category/1/change/
        """

        post = PostFactory()
        categ = post.categ
        categ_link = admin_change_url(obj=categ)

        url = reverse("admin:posts_post_changelist")

        resp = self.app.get(url)

        html_link = resp.html.find("a", href=categ_link)

        self.assertTrue(categ_link, html_link)


@override_settings(LANGUAGE_CODE="ru", LANGUAGES=(("ru", "Russian"),))
class TagSearchPostsTest(WebTest):
    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.create(name="слон")
        self.post_1 = PostFactory(status=Post.CurrentStatus.PUB.value, tags=(self.tag,))
        self.post_2 = PostFactory(
            status=Post.CurrentStatus.DRAFT.value, tags=(self.tag,)
        )

    def test_tag_seacrh(self):
        """
        posts page contains a list of tag(s) triggering
        filtering posts based on tag

        """
        start_url = reverse("posts:post_list")
        # initial request to get a list of tags
        resp = self.app.get(start_url)
        a_tag = resp.html.find("a", class_="tag-link")
        href = a_tag.attrs["href"]

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.context["tags"])
        self.assertEqual(a_tag.string, "слон")
        self.assertIsNotNone(href)

        resp2 = self.app.get(href)
        posts = resp2.context["posts"]

        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(posts.count(), 1)
