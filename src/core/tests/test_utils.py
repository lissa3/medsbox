from src.core.utils.admin_help import admin_change_url
from src.posts.tests.factories import PostFactory
from src.profiles.tests.factories.profile_factory import ProfileFactory


class TestBuildAdminLinkObjects:
    def test_admin_link_objects(self):
        """
        help function should build a link to
        page detail of a given object

        """
        profile = ProfileFactory()
        post = PostFactory()
        expected_profile_link = f"/admin/profiles/profile/{profile.id}/change/"
        expected_post = f"/admin/posts/post/{post.id}/change/"

        built_profile_link = admin_change_url(obj=profile)
        built_post_link = admin_change_url(obj=post)

        assert expected_post == built_post_link
        assert expected_profile_link == built_profile_link
