from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models

from user.permissions import GROUPS_TYPE


# https://docs.djangoproject.com/en/6.1/topics/db/managers/
# https://docs.djangoproject.com/en/6.1/ref/contrib/auth/
class UserManager(BaseUserManager):
    """
    Custom user model manager.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail deve ser informado.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_approved", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superusuários devem ter is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superusuários devem ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# https://docs.djangoproject.com/en/6.1/topics/auth/customizing/#substituting-a-custom-user-model
class User(AbstractUser, PermissionsMixin):
    """ "
    Custom user model.
    """

    nome = models.CharField("nome completo", max_length=255)
    email = models.EmailField("e-mail", unique=True)
    matricula = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # noqa: RUF012

    objects = UserManager()

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        # https://docs.djangoproject.com/en/6.1/topics/auth/customizing/#custom-permissions
        permissions = [  # noqa: RUF012
            ("approve_administrator", "Pode aprovar o cadastro de administrador"),
        ]

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()

        if (self.groups.filter(name=GROUPS_TYPE.ADMIN).exists()) and not self.matricula:
            raise ValueError("A matrícula é obrigatória para administradores.")

    def get_groups(self):
        return ", ".join(group.name for group in self.groups.all())
