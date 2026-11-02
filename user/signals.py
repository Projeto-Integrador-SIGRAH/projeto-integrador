from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .permissions import configure_role_groups


@receiver(post_migrate)
def create_role_groups(sender, app_config, using, **kwargs):
    if sender.label != "user":
        return
    configure_role_groups(using=using)
