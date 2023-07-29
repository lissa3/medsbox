from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils import timezone
from django_extensions.management.jobs import WeeklyJob

from src.contacts.models import NewsLetter
from src.posts.models.post_model import Post
from src.profiles.models import Profile


class Job(WeeklyJob):
    """
    users: active status and profile wanted_niews
    will get email with news weekly;
    let op: Job package;
    """

    help = "Send news letter"  # noqa

    def execute(self):
        _date = timezone.localdate()
        str_date = _date.strftime("%d/%m/%Y")
        stamp = f"Newsletter {_date:%A}, {_date:%b}. {_date:%d} {str_date}"
        domain = settings.ABSOLUTE_URL_BASE
        profiles = Profile.objects.send_news().select_related("user")
        letter = NewsLetter.objects.filter(letter_status=1).last()
        ctx = {"letter": letter}
        posts = Post.objects.filter(send_status=1, letter=letter)
        if letter.posts:
            ctx.update({"posts": letter.posts.all(), "domain": domain})
        if letter and profiles:
            text_msg = render_to_string("contacts/emails/letter.txt", ctx)
            html_msg = render_to_string("contacts/emails/letter.html", ctx)
            try:
                for profile in profiles:
                    mail.send_mail(
                        subject=stamp,
                        message=text_msg,
                        html_message=html_msg,
                        from_email="From MedSandbox",
                        recipient_list=[profile.user.email],
                    )
                letter.sended_at = timezone.now()
                letter.letter_status = 2
                letter.save()
                for post in posts:
                    post.send_status = 2
                    post.save()

            except Exception as e:
                print(e)
                # TODO: add Log
