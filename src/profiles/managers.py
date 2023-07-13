from django.db.models import QuerySet


class ProfileManager(QuerySet):
    def send_news(self):
        return self.filter(user__is_active=True, want_news=True)
