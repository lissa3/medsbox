from django.db.models import QuerySet


class PostFilterManager(QuerySet):
    def get_drafts(self):
        """filter qs for posts in draft
        (in progress)"""
        return self.filter(status=0, is_deleted=False)

    def get_review(self):
        """filter qs for posts in review"""
        return self.filter(status=1, is_deleted=False)

    def get_public(self):
        """filter qs for public posts"""
        return self.filter(status=2, is_deleted=False)

    def get_soft_deleted(self):
        """filter qs for soft deleted;
        posts can have diff status
        """
        return self.filter(is_deleted=True)
