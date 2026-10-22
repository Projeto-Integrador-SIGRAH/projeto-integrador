from rest_framework import serializers

from user.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"email": {"validators": ()}}  # noqa: RUF012

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Usuário não encontrado.")

            if not user.check_password(password):
                raise serializers.ValidationError("Senha incorreta.")
        else:
            raise serializers.ValidationError("Email e senha são obrigatórios.")

        data["user"] = user
        return data
