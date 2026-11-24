from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import (
    MethodNotAllowed,
    PermissionDenied,
    ValidationError,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from canos.api.views import GenericModelViewSet

from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserSerializer

User = get_user_model()


class UserLoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data if request.data else request.POST
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        login(request, user)

        refresh = RefreshToken.for_user(user)

        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


class UserRegistrationAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        message = (
            "Cadastro realizado. Aguarde a aprovação de outro administrador!"
            if not user.is_approved
            else "Cadastro realizado!"
        )

        return Response({"detail": message}, status=status.HTTP_201_CREATED)


class UserLogoutAPIView(APIView):
    def post(self, request):
        if isinstance(request.successful_authenticator, SessionAuthentication):
            logout(request)

        elif isinstance(request.successful_authenticator, JWTAuthentication):
            refresh_token = request.data.get("refresh")

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

        return Response(
            {"detail": "Logout realizado com sucesso."},
            status=status.HTTP_200_OK,
        )


class UserModelViewSet(GenericModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_superuser:
            if user.groups.filter(name="ADMIN").exists():
                return queryset.filter(groups__name="ADMIN")
            elif user.groups.filter(name="CIDADAO").exists():
                return queryset.filter(id=user.id)

        return queryset

    def perform_create(self, serializer):
        raise MethodNotAllowed("Método não permitido.")

    def perform_destroy(self, instance):
        raise MethodNotAllowed("Método não permitido.")

    def perform_update(self, serializer):
        raise MethodNotAllowed("Método não permitido.")

    def _check_approve_admin_permission(self):
        user = self.request.user
        user_obj = self.get_object()

        if not (
            (user.is_superuser or user.has_perm("approve_administrator"))
            and user_obj.groups.filter(name="ADMIN").exists()
        ):
            raise PermissionDenied("Você não tem permissão para realizar esta ação.")

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        self._check_approve_admin_permission()

        user = self.get_object()

        if user.is_rejected:
            raise ValidationError("Não é possível aprovar um cadastro rejeitado.")

        user.is_approved = True
        user.is_active = True
        user.save(update_fields=["is_approved", "is_active"])

        return Response(
            {"detail": "Administrador aprovado com sucesso."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        self._check_approve_admin_permission()

        user = self.get_object()

        if user.is_approved:
            raise ValidationError(
                "Não é possível rejeitar um administrador já aprovado."
            )

        user.is_active = False
        user.is_approved = False
        user.is_rejected = True
        user.save(
            update_fields=[
                "is_active",
                "is_approved",
                "is_rejected",
            ]
        )

        return Response(
            {"detail": "Cadastro rejeitado com sucesso."},
            status=status.HTTP_200_OK,
        )
