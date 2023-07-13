from django.core import mail
from django_extensions.management.jobs import WeeklyJob

from src.profiles.models import Profile


class Job(WeeklyJob):
    """
    users: active status and profile wanted_niews
    will get email with news weekly;
    let op: Job package;
    """

    help = "Send news letter"  # noqa

    def execute(self):
        profiles = Profile.objects.send_news().select_related("user")
        for profile in profiles:
            mail.send_mail(
                subject="Meds news",
                message="Some message",
                html_message="Some html msg",
                from_email="From MedSandbox",
                recipient_list=[profile.user.email],
            )
