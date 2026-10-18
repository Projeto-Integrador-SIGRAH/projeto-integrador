from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer


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
