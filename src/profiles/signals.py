import logging
from datetime import date

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()
logger = logging.getLogger("user_issues")


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    try:
        if created and instance.email:
            Profile.objects.get_or_create(user=instance)
            logger.info(f"user {instance.id} created profile successfully")
    except Exception as e:
        print("Smth went wrong with profile creation", e)
        logger.error(f"user ID:{instance.id} failed to create  his profile: {str(e)}")


@receiver(post_delete, sender=Profile)
def set_user_inactive(sender, instance, **kwargs):
    """as profile deleted - user set to not activate")"""
    try:
        user_obj = instance.user
        user_obj.is_active = False
        user_obj.deactivated_on = date.today()
        user_obj.save()
        logger.warning(
            f"{user_obj.id} deleted his account and became deactivated on {date.today()}"
        )
    except Exception as e:
        logger.error(f"{user_obj.id} failed to delete his profile: {str(e)}")
