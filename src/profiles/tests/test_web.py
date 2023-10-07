import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest

from src.accounts.tests.factories import UserFactory
from src.core.utils.base import get_temp_img_bytes
from src.profiles.models import Profile

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class MyTestCase(WebTest):
    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.profile = Profile.objects.get(user=self.user)
        self.profile_uuid = self.profile.uuid
        self.url = reverse(
            "profiles:profile_detail", kwargs={"uuid": self.profile_uuid}
        )
        self.err_file = (
            "Upload a valid image. The file you uploaded "
            + "was either not an image or a corrupted image."
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)  # delete the temp dir
        super().tearDownClass()

    def test_upload_avatar_ok(self):
        """check form upload avatar diff attrs"""
        avatar = get_temp_img_bytes()
        data = {"avatar": SimpleUploadedFile("zoo.jpeg", avatar, "image/jpeg")}

        response = self.client.post(
            self.url,
            data,
            format="multipart",
            follow=True,
            headers={"x-requested-with": "XMLHttpRequest"},
        )

        resp = response.json()

        self.assertEqual(resp["status_code"], 200)

    @override_settings(MAX_UPLOAD_SIZE=5)
    def test_upload_big_avatar(self):
        avatar = get_temp_img_bytes()
        data = {"avatar": SimpleUploadedFile("zoo.jpeg", avatar, "image/jpeg")}

        response = self.client.post(
            self.url,
            data,
            format="multipart",
            headers={"x-requested-with": "XMLHttpRequest"},
        )

        resp_dict = response.json()
        err_msg = (
            f"Uploaded file should not be more than {settings.MAX_UPLOAD_SIZE} bytes"
        )

        self.assertEqual(resp_dict["status_code"], 404)
        self.assertEqual(resp_dict["err"]["avatar"][0], err_msg)

    @override_settings(MIN_UPLOAD_SIZE=1000)
    def test_upload_too_small_avatar(self):
        avatar = get_temp_img_bytes()
        data = {"avatar": SimpleUploadedFile("zoo.jpeg", avatar, "image/jpeg")}

        response = self.client.post(
            self.url,
            data,
            format="multipart",
            headers={"x-requested-with": "XMLHttpRequest"},
        )

        resp_dict = response.json()
        err_msg = (
            f"Uploaded file should not be less than {settings.MIN_UPLOAD_SIZE} bytes."
        )

        self.assertEqual(resp_dict["status_code"], 404)
        self.assertEqual(resp_dict["err"]["avatar"][0], err_msg)

    def test_remove_avatar(self):
        """remove avatar"""
        self.profile.avatar = get_temp_img_bytes()

        response = self.client.post(
            self.url,
            data=None,
            format="multipart",
            headers={"x-requested-with": "XMLHttpRequest"},
        )

        resp_dict = response.json()
        self.profile.refresh_from_db()
        profile_avatar = self.profile.avatar

        self.assertEqual(resp_dict["status_code"], 200)
        self.assertEqual(profile_avatar, "")

    def test_upload_txt_avatar(self):
        """test json response after uploading file not allowed as avatar(.txt)"""
        data = {"avatar": SimpleUploadedFile("zoo.txt", b"zoo", "text/txt")}

        response = self.client.post(
            self.url,
            data,
            format="multipart",
            headers={"x-requested-with": "XMLHttpRequest"},
        )

        resp_dict = response.json()

        self.assertEqual(resp_dict["status_code"], 404)
        self.assertEqual(resp_dict["err"]["avatar"][0], self.err_file)

    def test_delete_button(self):
        """button delete should be present on detail profile"""
        self.app.set_user(self.user)

        response = self.app.get(self.url)

        but_del_profile = response.html.find("button", id="to_delete")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(but_del_profile)

    def test_on_delete_redirect(self):
        """redirect to home page after delete profile"""
        self.app.set_user(self.user)
        del_url = reverse("profiles:profile_delete", kwargs={"uuid": self.profile_uuid})
        home_url = reverse("home")

        resp = self.app.get(del_url)

        self.assertEqual(resp.status_code, 200)

        form = resp.forms["del_profile"]
        response = form.submit()

        self.assertRedirects(response, home_url)

    def test_delete_final_result(self):
        """request profile delete: username present on page;
        after profile delete: no trace of username"""
        self.app.set_user(self.user)
        del_url = reverse("profiles:profile_delete", kwargs={"uuid": self.profile_uuid})

        resp = self.app.get(del_url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.user.username)

        form = resp.forms["del_profile"]
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user.username)
