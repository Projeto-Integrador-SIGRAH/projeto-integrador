from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from user.permissions import GROUPS_TYPE

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, trim_whitespace=False)
    group = serializers.ChoiceField(
        choices=[(GROUPS_TYPE.CIDADAO, "Cidadão"), (GROUPS_TYPE.ADMIN, "Admin")],
        write_only=True,
    )

    class Meta:
        model = User
        fields = [  # noqa: RUF012
            "nome",
            "email",
            "matricula",
            "password",
            "confirm_password",
            "group",
        ]
        extra_kwargs = {  # noqa: RUF012
            "matricula": {"required": False, "allow_blank": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Já existe um cadastro com este e-mail.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "As senhas não coincidem."}
            )

        if attrs["group"] == GROUPS_TYPE.ADMIN and not attrs.get("matricula"):
            raise serializers.ValidationError(
                {"matricula": "A matrícula é obrigatória para administradores."}
            )

        candidate = User(email=attrs["email"], nome=attrs["nome"])
        try:
            validate_password(attrs["password"], user=candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        group = str(validated_data.pop("group")).strip().upper()
        is_cidadao = group == GROUPS_TYPE.CIDADAO

        user = User.objects.create_user(
            password=password,
            is_active=is_cidadao,
            is_approved=is_cidadao,
            username=validated_data.get("email"),
            **validated_data,
        )

        group = get_object_or_404(Group, name=group)
        user.groups.add(group)
        return user
