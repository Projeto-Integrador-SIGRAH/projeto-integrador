from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User
from user.permissions import GROUPS_TYPE


class UserLoginAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_group, _ = Group.objects.get_or_create(name=GROUPS_TYPE.ADMIN)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:login")

        self.email = "admin@example.com"
        self.password = "StrongPass123!"

    def create_user(self, is_active=True, is_approved=True):
        user = User.objects.create_user(
            nome="Administrador",
            email=self.email,
            username=self.email,
            password=self.password,
            matricula="20240001",
            is_active=is_active,
            is_approved=is_approved,
        )
        user.groups.add(self.admin_group)
        return user

    def login(self, email=None, password=None):
        return self.client.post(
            self.url,
            {
                "email": email or self.email,
                "password": password or self.password,
            },
            format="json",
        )

    def test_login_with_valid_credentials(self):
        self.create_user()

        response = self.login()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_password(self):
        self.create_user()

        response = self.login(password="WrongPassword123!")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_login_with_wrong_email(self):
        self.create_user()

        response = self.login(email="invalid@example.com")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_login_admin_inactive_and_not_approved(self):
        self.create_user(is_active=False, is_approved=False)

        response = self.login()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_login_admin_active_and_not_approved(self):
        self.create_user(is_active=True, is_approved=False)

        response = self.login()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_login_admin_inactive_and_approved(self):
        self.create_user(is_active=False, is_approved=True)

        response = self.login()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_login_admin_active_and_approved(self):
        self.create_user(is_active=True, is_approved=True)

        response = self.login()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class UserRegistrationAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.get_or_create(name=GROUPS_TYPE.CIDADAO)
        Group.objects.get_or_create(name=GROUPS_TYPE.ADMIN)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:register")
        self.valid_password = "StrongPass123!"

    def get_registration_data(self, group):
        data = {
            "nome": "Usuário de Teste",
            "email": "usuario@example.com",
            "password": self.valid_password,
            "confirm_password": self.valid_password,
            "group": group,
        }

        if group == GROUPS_TYPE.ADMIN:
            data["matricula"] = "20240001"

        return data

    def register(self, data):
        return self.client.post(
            self.url,
            data,
            format="json",
        )

    def test_register_cidadao_with_valid_data(self):
        data = self.get_registration_data(GROUPS_TYPE.CIDADAO)

        response = self.register(data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(email=data["email"])

        self.assertEqual(user.nome, data["nome"])
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_approved)
        self.assertTrue(user.groups.filter(name=GROUPS_TYPE.CIDADAO).exists())
        self.assertTrue(user.check_password(self.valid_password))

    def test_register_admin_with_valid_data(self):
        data = self.get_registration_data(GROUPS_TYPE.ADMIN)

        response = self.register(data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(email=data["email"])

        self.assertEqual(user.nome, data["nome"])
        self.assertEqual(user.matricula, data["matricula"])
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_approved)
        self.assertTrue(user.groups.filter(name=GROUPS_TYPE.ADMIN).exists())
        self.assertTrue(user.check_password(self.valid_password))

    def test_register_cidadao_with_invalid_data(self):
        data = self.get_registration_data(GROUPS_TYPE.CIDADAO)
        data["confirm_password"] = "DifferentPassword123!"

        response = self.register(data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(User.objects.filter(email=data["email"]).exists())

    def test_register_admin_with_invalid_data(self):
        data = self.get_registration_data(GROUPS_TYPE.ADMIN)
        data.pop("matricula")

        response = self.register(data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(User.objects.filter(email=data["email"]).exists())

    def test_register_with_existing_email(self):
        User.objects.create_user(
            nome="Usuário Existente",
            email="usuario@example.com",
            username="usuario@example.com",
            password=self.valid_password,
        )

        data = self.get_registration_data(GROUPS_TYPE.CIDADAO)

        response = self.register(data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            User.objects.filter(email__iexact=data["email"]).count(),
            1,
        )
