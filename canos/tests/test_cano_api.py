from datetime import timedelta

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from canos.models import Cano, Equipe, Material
from user.models import User
from user.permissions import GROUPS_TYPE


class CanoAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_group, _ = Group.objects.get_or_create(name=GROUPS_TYPE.ADMIN)
        cls.cidadao_group, _ = Group.objects.get_or_create(name=GROUPS_TYPE.CIDADAO)

        content_type = ContentType.objects.get_for_model(Cano)

        permissions = {
            permission.codename: permission
            for permission in Permission.objects.filter(
                content_type=content_type,
                codename__in=[
                    "add_cano",
                    "change_cano",
                    "delete_cano",
                    "view_cano",
                ],
            )
        }

        cls.cidadao_group.permissions.set(
            [
                permissions["view_cano"],
            ]
        )

        # Permissões do administrador
        cls.admin_group.permissions.set(
            [
                permissions["add_cano"],
                permissions["change_cano"],
                permissions["delete_cano"],
                permissions["view_cano"],
            ]
        )

    def setUp(self):
        self.client = APIClient()

        self.list_url = reverse("api:cano-list")

        self.admin = User.objects.create_user(
            nome="Administrador",
            email="admin@example.com",
            username="admin@example.com",
            password="StrongPass123!",
            is_active=True,
            is_approved=True,
        )
        self.admin.groups.add(self.admin_group)

        self.cidadao = User.objects.create_user(
            nome="Cidadão",
            email="cidadao@example.com",
            username="cidadao@example.com",
            password="StrongPass123!",
            is_active=True,
            is_approved=True,
        )
        self.cidadao.groups.add(self.cidadao_group)
        self.material = Material.objects.create(tipo="PVC")
        self.equipe = Equipe.objects.create(nome="Equipe de manutenção")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def get_cano_data(self, **overrides):
        """
        Retorna os dados válidos para criação de um cano.

        Para campos com choices, utiliza automaticamente
        a primeira opção disponível no model.
        """

        def get_first_choice(field_name, fallback):
            field = Cano._meta.get_field(field_name)

            choices = [
                value for value, label in field.flatchoices if value not in ("", None)
            ]

            return choices[0] if choices else fallback

        data = {
            "codigo": "CANO-001",
            "coordenadas": "[[-5.7900, -38.2000], [-5.7910, -38.2010]]",
            "diametro": 100,
            "tipo": Cano.Tipo.AGUA,
            "material": self.material.pk,
            "status": Cano.Status.DISPONIVEL,
            "equipe_responsavel": self.equipe.pk,
            "data_instalacao": timezone.now().date().isoformat(),
            "observacoes": "Cano de teste.",
        }

        data.update(overrides)

        return data

    def create_cano(self, user=None, **overrides):
        """
        Cria um cano através da API.
        """
        self.authenticate(user or self.admin)

        return self.client.post(
            self.list_url,
            self.get_cano_data(**overrides),
            format="json",
        )

    def get_detail_url(self, cano_id):
        return reverse("api:cano-detail", kwargs={"pk": cano_id})

    def test_admin_can_create_cano(self):
        """Administrador deve conseguir cadastrar um cano."""
        response = self.create_cano()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        cano = Cano.objects.get(codigo="CANO-001")

        self.assertEqual(cano.user, self.admin)
        self.assertEqual(cano.codigo, "CANO-001")

    def test_cidadao_cannot_create_cano(self):
        """Cidadão não deve conseguir cadastrar um cano."""
        response = self.create_cano(user=self.cidadao)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(Cano.objects.filter(codigo="CANO-001").exists())

    def test_create_cano_with_duplicate_codigo(self):
        """Não deve permitir cadastrar dois canos com o mesmo código."""
        self.create_cano()

        response = self.create_cano(
            codigo="cano-001",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("codigo", response.data)

        self.assertEqual(
            Cano.objects.filter(codigo__iexact="CANO-001").count(),
            1,
        )

    def test_create_cano_with_future_installation_date(self):
        """Não deve permitir uma data de instalação futura."""
        future_date = timezone.now().date() + timedelta(days=1)

        response = self.create_cano(
            codigo="CANO-002",
            data_instalacao=future_date.isoformat(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("data_instalacao", response.data)

        self.assertFalse(Cano.objects.filter(codigo="CANO-002").exists())

    def test_admin_can_list_canos(self):
        """Administrador deve conseguir listar os canos."""
        self.create_cano()

        self.authenticate(self.admin)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_cidadao_can_list_canos(self):
        """Cidadão deve conseguir listar os canos."""
        self.create_cano()

        self.authenticate(self.cidadao)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_admin_can_retrieve_cano(self):
        """Administrador deve conseguir visualizar um cano."""
        create_response = self.create_cano()

        cano_id = create_response.data["id"]

        self.authenticate(self.admin)

        response = self.client.get(self.get_detail_url(cano_id))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["id"], cano_id)

    def test_cidadao_can_retrieve_cano(self):
        """Cidadão deve conseguir visualizar um cano."""
        create_response = self.create_cano()

        cano_id = create_response.data["id"]

        self.authenticate(self.cidadao)

        response = self.client.get(self.get_detail_url(cano_id))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["id"], cano_id)

    def test_admin_can_update_cano(self):
        """Administrador deve conseguir alterar um cano."""
        create_response = self.create_cano()

        cano_id = create_response.data["id"]

        self.authenticate(self.admin)

        response = self.client.patch(
            self.get_detail_url(cano_id),
            {
                "observacoes": "Observação atualizada.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        cano = Cano.objects.get(pk=cano_id)

        self.assertEqual(
            cano.observacoes,
            "Observação atualizada.",
        )

    def test_cidadao_cannot_update_cano(self):
        """Cidadão não deve conseguir alterar um cano."""
        create_response = self.create_cano()

        cano_id = create_response.data["id"]

        self.authenticate(self.cidadao)

        response = self.client.patch(
            self.get_detail_url(cano_id),
            {
                "observacoes": "Tentativa de alteração.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        cano = Cano.objects.get(pk=cano_id)

        self.assertEqual(
            cano.observacoes,
            "Cano de teste.",
        )

    def test_admin_can_delete_cano(self):
        """Administrador deve conseguir excluir um cano."""
        create_response = self.create_cano()

        cano_id = create_response.data["id"]

        self.authenticate(self.admin)

        response = self.client.delete(self.get_detail_url(cano_id))

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(Cano.objects.filter(pk=cano_id).exists())

    def test_cidadao_cannot_delete_cano(self):
        """Cidadão não deve conseguir excluir um cano."""
        create_response = self.create_cano()

        cano_id = create_response.data["id"]

        self.authenticate(self.cidadao)

        response = self.client.delete(self.get_detail_url(cano_id))

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(Cano.objects.filter(pk=cano_id).exists())
