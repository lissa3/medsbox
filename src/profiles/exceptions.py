class ProfileException(Exception):
    """
    get triggered if Profile object failed to create
    """

    pass


class NoAjaxError(Exception):
    """
    get triggered if request is not ajax
    """

    pass
