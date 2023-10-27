from src.posts.models.relation_model import Relation


def check_data_menu(request):
    """
    Only auth user without subscription to news
    will see in UI(menu dropdown) subscription suggestion
    """
    if request.user.is_authenticated:
        news_negative = request.user.profile.want_news
        has_bookmarks = Relation.objects.filter(
            user_id=request.user.id, in_bookmark=True
        ).exists()

    else:
        news_negative = None
        has_bookmarks = None

    return {"news_negative": news_negative, "has_bookmarks": has_bookmarks}
