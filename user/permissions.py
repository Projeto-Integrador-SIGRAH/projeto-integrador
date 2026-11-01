from django.contrib.auth.models import Group, Permission


class GROUPS_TYPE:
    CIDADAO = "CIDADAO"
    ADMIN = "ADMIN"


CANO_PERMISSIONS = {
    "add_cano": "Pode adicionar cano",
    "change_cano": "Pode alterar cano",
    "delete_cano": "Pode deletar cano",
    "view_cano": "Pode visualizar cano",
}


GROUPS_PERMISSIONS = {
    GROUPS_TYPE.CIDADAO: [
        "view_cano",
    ],
    GROUPS_TYPE.ADMIN: [
        "approve_administrator",
        "can_access_admin_panel",
        "can_access_admin_management",
        "add_cano",
        "change_cano",
        "delete_cano",
        "view_cano",
    ],
}


def configure_role_groups(*, using):
    permissions = Permission.objects.using(using).all()
    permissions_by_codename = {
        permission.codename: permission for permission in permissions
    }

    for group_name, permission_codenames in GROUPS_PERMISSIONS.items():
        group, _ = Group.objects.using(using).get_or_create(name=group_name)
        group.permissions.set(
            [permissions_by_codename[codename] for codename in permission_codenames]
        )
