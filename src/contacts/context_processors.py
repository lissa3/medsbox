def check_subscription(request):
    """
    Only auth user without subscription to news
    will see in UI(menu dropdown) subscription suggestion
    """
    if request.user.is_authenticated:
        news_negative = request.user.profile.want_news
    else:
        news_negative = None
    return {"news_negative": news_negative}
