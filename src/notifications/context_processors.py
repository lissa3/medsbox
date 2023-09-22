from src.notifications.models import Notification


def check_nofications(request):
    """
    Auth user will see in UI(menu) count unread notifications
    """
    if request.user.is_authenticated:
        notifs = Notification.objects.count_unread_notifics(recipient=request.user)
        return {"notifs": notifs}
