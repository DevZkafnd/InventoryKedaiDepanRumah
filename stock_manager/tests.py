from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Admin


class WarehouseViewTests(TestCase):
    def setUp(self):
        self.managers_group, _ = Group.objects.get_or_create(name="managers")
        self.owners_group, _ = Group.objects.get_or_create(name="owners")

    def test_manager_sees_excel_import_controls_in_warehouse(self):
        user = User.objects.create_user(username="manager", password="secret123")
        user.groups.add(self.managers_group)
        Admin.get_solo().save()

        self.client.force_login(user)
        response = self.client.get(reverse("warehouse"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload Excel")
        self.assertContains(response, 'data-can-import-excel="true"', html=False)
        self.assertContains(response, 'data-allow-uploads-enabled="false"', html=False)

    def test_owner_cannot_access_warehouse_view(self):
        user = User.objects.create_user(username="owner", password="secret123")
        user.groups.add(self.owners_group)

        self.client.force_login(user)
        response = self.client.get(reverse("warehouse"))

        self.assertEqual(response.status_code, 403)
