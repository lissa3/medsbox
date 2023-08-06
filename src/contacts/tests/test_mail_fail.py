from smtplib import SMTPException
from unittest import mock

from django.core import mail
from django.test import TestCase

from src.accounts.models import User
from src.contacts.jobs.send_news import Job as SendMailJob
from src.profiles.tests.factories.profile_factory import ProfileFactory

from ..exceptions import *  # noqa
from .factories import NewsLetterFactory


@mock.patch("django.core.mail.send_mail")
class MailFailureTests(TestCase):
    def test_news_not_send(self, mock_fail):
        profile = ProfileFactory(want_news=True)  # noqa
        letter = NewsLetterFactory(letter_status=1)  # noqa

        mock_fail.side_effect = SMTPException

        send_mail_job = SendMailJob()
        send_mail_job.execute()

        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(mock_fail.called)
        with self.assertRaises(SMTPException):
            mock_fail()


class TestSendEmailJob(TestCase):
    def test_manager_no_news_inactive_user(self):
        """
        letter exists but modal manager method
        method filters user is inactive;
        ex: user inactive via other route than deleted account
        """
        profile = ProfileFactory(want_news=True)
        user = User.objects.get(profile=profile)
        user.is_active = False
        user.save()
        letter = NewsLetterFactory(letter_status=1)  # noqa
        send_mail_job = SendMailJob()
        with self.assertRaises(NewsFansNotFoundException) as e:
            send_mail_job.execute()
        self.assertEqual(str(e.exception), "No profiles not send news")
        self.assertEqual(len(mail.outbox), 0)

    def test_manager_no_news_fans(self):
        """
        letter exists profile modal manager
        filters no news fans
        """
        profile = ProfileFactory()  # noqa
        letter = NewsLetterFactory(letter_status=1)  # noqa
        send_mail_job = SendMailJob()
        with self.assertRaises(NewsFansNotFoundException) as e:
            send_mail_job.execute()

        self.assertEqual(str(e.exception), "No profiles not send news")
        self.assertEqual(len(mail.outbox), 0)

    def test_no_letter_no_job(self):
        """
        if no letter -> no SendMail
        """
        profile = ProfileFactory(want_news=True)  # noqa
        send_mail_job = SendMailJob()
        with self.assertRaises(LetterNotFoundException) as e:
            send_mail_job.execute()

        self.assertEqual(str(e.exception), "No letter to send")
        assert len(mail.outbox) == 0
