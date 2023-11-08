from smtplib import SMTPException

from django.conf import settings
from django.core import mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from src.contacts.exceptions import *  # noqa
from src.contacts.models import NewsLetter
from src.posts.models.post_model import Post
from src.profiles.models import Profile


class Command(BaseCommand):
    """
    users: active status and profile wanted_niews
    will get email with news weekly?;
    News letter may not contain links to posts
    TODO: better way to arrange unsubscribe

    """

    help = "Send a newsletter to subscribed users"  # noqa

    def handle(self, *args, **options):
        _date = timezone.localdate()
        str_date = _date.strftime("%d/%m/%Y")
        stamp = f"Newsletter {_date:%A}, {_date:%b}. {_date:%d} {str_date}"
        domain = settings.ABSOLUTE_URL_BASE
        profiles = Profile.objects.send_news().select_related("user")
        letter = NewsLetter.objects.filter(letter_status=1).last()
        ctx = {"letter": letter, "domain": domain}

        if profiles and letter:
            try:
                posts = Post.objects.get_public().filter(send_status=1, letter=letter)
                ctx.update({"posts": posts})
                for profile in profiles:
                    ctx.update({"uuid": profile.uuid})
                    text_msg = render_to_string("contacts/emails/letter.txt", ctx)
                    html_msg = render_to_string("contacts/emails/letter.html", ctx)
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
                if posts.count() > 0:
                    for post in posts:
                        post.send_status = 2
                        post.save()
                self.stdout.write(self.style.SUCCESS("Successfully sent newletter"))

            except SMTPException as e:
                print("smth went wrong ", e)
                # TODO: add Log

        else:
            if not profiles:
                raise NewsFansNotFoundException("No profiles not send news")
            elif not letter:
                raise LetterNotFoundException("No letter to send")
