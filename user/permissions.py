from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class GROUPS_TYPE:
    CIDADAO = "CIDADAO"
    ADMIN = "ADMIN"


GROUPS_PERMISSIONS = {
    GROUPS_TYPE.CIDADAO: [],
    GROUPS_TYPE.ADMIN: [
        "approve_administrator",
    ],
}


def configure_role_groups(*, using):
    User = get_user_model()

    content_type = ContentType.objects.db_manager(using).get_for_model(User)
    permissions = Permission.objects.using(using).filter(content_type=content_type)
    permissions_by_codename = {
        permission.codename: permission for permission in permissions
    }

    for group_name, permission_codenames in GROUPS_PERMISSIONS.items():
        group, _ = Group.objects.using(using).get_or_create(name=group_name)
        group.permissions.set(
            [permissions_by_codename[codename] for codename in permission_codenames]
        )
