from django.utils.html import format_html


def admin_link(attr: str, short_description: str, empty_description="-"):
    """
    Help decorator function for admin;
    The wrapped method receives the related object and should
    return the link text.
    """

    def wrap(func):
        # func.__name__ categ_link
        def field_func(self, obj: object):
            #  object == post
            related_obj = getattr(obj, attr)
            if related_obj is None:
                return empty_description
            url = self.admin_change_url(related_obj)

            return format_html("<a href={}>{}</a>", url, func(self, related_obj))

        field_func.short_description = short_description
        return field_func

    return wrap
