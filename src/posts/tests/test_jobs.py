from src.posts.jobs.send_news import Job as SendMailJob
from src.profiles.tests.factories.profile_factory import ProfileFactory


class TestSendEmailJob:
    def test_send_news(self, mailoutbox):
        """
        active user can get news letter via email prompt;
        let op: mailoutbox via pytest
        """
        profile = ProfileFactory(want_news=True)

        send_mail_job = SendMailJob()
        send_mail_job.execute()

        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.to == [profile.user.email]
        # TODO: assert subject
        # TODO: assert message
        # TODO: assert html_message
        # TODO: assert from_email
