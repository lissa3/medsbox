import time_machine

from src.contacts.jobs.send_news import Job as SendMailJob
from src.contacts.models import NewsLetter
from src.posts.models.post_model import Post
from src.posts.tests.factories import PostFactory
from src.profiles.tests.factories.profile_factory import ProfileFactory

from .factories import NewsLetterFactory


class TestSendEmailJob:
    @time_machine.travel("2023-07-17 00:00 +0000")
    def test_send_news(self, mailoutbox):
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

        letter = NewsLetterFactory(letter_status=1)
        post.letter = letter
        post.save()
        # TODO: add a tag with link
        # domain = settings.ABSOLUTE_URL_BASE
        # link = f'<a href="{domain}'

        send_mail_job = SendMailJob()
        send_mail_job.execute()

        assert len(mailoutbox) == 1

        mail = mailoutbox[0]

        html_msg = mail.alternatives[0][0]

        assert mail.to == [profile.user.email]
        assert mail.subject == subject

        assert letter.text in mail.body
        assert letter.text in html_msg
        assert post_title in mail.body
        assert post_title in html_msg
        # TODO: change title for a link to post
        # assert link in mail.body
        # assert link in html_msg

        post_after = Post.objects.filter(send_status=2).last()
        letter_after = NewsLetter.objects.filter(letter_status=2).last()

        assert post.id == post_after.id
        assert post_after.send_status == 2
        assert letter.id == letter_after.id
        assert letter_after.letter_status == 2