import pytest
import time_machine
from django.conf import settings
from django.urls import reverse

from src.accounts.models import User
from src.contacts.exceptions import *  # noqa
from src.contacts.jobs.send_news import Job as SendMailJob
from src.contacts.models import NewsLetter
from src.posts.models.post_model import Post
from src.posts.tests.factories import PostFactory
from src.profiles.tests.factories.profile_factory import ProfileFactory

from .factories import NewsLetterFactory


class TestSendEmailJob:
    @time_machine.travel("2023-07-17 00:00 +0000")
    def test_send_news_with_posts_links(self, mailoutbox):
        """
        active user (can) get news letter via email
        with corresp links to posts;
        if sending OK: letter and related posts
        change their status
        """
        subject = "Newsletter Monday, Jul. 17 17/07/2023"
        profile = ProfileFactory(want_news=True)
        post = PostFactory(send_status=1)
        post_title = post.title
        domain = settings.ABSOLUTE_URL_BASE
        letter = NewsLetterFactory(letter_status=1)
        post.letter = letter
        post.save()

        short_url = reverse("contacts:end_news", kwargs={"uuid": profile.uuid})
        full_link_unsub = f"{domain}{short_url}"
        send_mail_job = SendMailJob()
        send_mail_job.execute()

        assert len(mailoutbox) == 1

        mail = mailoutbox[0]
        html_msg = mail.alternatives[0][0]

        assert mail.to == [profile.user.email]
        assert mail.subject == subject

        assert letter.text in mail.body
        assert letter.text in html_msg
        # TODO: change title for a link to post
        assert post_title in mail.body
        assert post_title in html_msg
        # email (html)text contains a link to unsubscribe
        assert full_link_unsub in mail.body
        assert full_link_unsub in html_msg

        post_after = Post.objects.filter(send_status=2).last()
        letter_after = NewsLetter.objects.filter(letter_status=2).last()

        assert post.id == post_after.id
        assert post_after.send_status == 2
        assert letter.id == letter_after.id
        assert letter_after.letter_status == 2

    @time_machine.travel("2023-07-17 00:00 +0000")
    def test_send_news_no_posts(self, mailoutbox):
        """
        No posts links in the letter no posts with
        send_status
        """
        subject = "Newsletter Monday, Jul. 17 17/07/2023"
        profile = ProfileFactory(want_news=True)
        post = PostFactory(send_status=0)
        post_title = post.title
        domain = settings.ABSOLUTE_URL_BASE
        letter = NewsLetterFactory(letter_status=1)

        short_url = reverse("contacts:end_news", kwargs={"uuid": profile.uuid})
        full_link_unsub = f"{domain}{short_url}"
        send_mail_job = SendMailJob()
        send_mail_job.execute()

        assert len(mailoutbox) == 1

        mail = mailoutbox[0]
        html_msg = mail.alternatives[0][0]

        assert mail.to == [profile.user.email]
        assert mail.subject == subject

        assert letter.text in mail.body
        assert letter.text in html_msg
        # TODO: change title for a link to post
        assert post_title not in mail.body
        assert post_title not in html_msg
        # email (html)text contains a link to unsubscribe
        assert full_link_unsub in mail.body
        assert full_link_unsub in html_msg

        post_after = Post.objects.filter(send_status=2).count()
        letter_after = NewsLetter.objects.filter(letter_status=2).last()

        assert post_after == 0
        assert letter.id == letter_after.id
        assert letter_after.letter_status == 2
