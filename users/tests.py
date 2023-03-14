from django.contrib.auth.models import User
from rest_framework.reverse import reverse, reverse_lazy
# from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class UserAPITest(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser("iamsuper", "super@circle.com", "admin123")

        self.client.force_authenticate(self.superuser)

        url = reverse("api:users-list")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "abcd1234",
            "first_name": "test",
            "last_name": "user"
        }
        response = self.client.post(url, data, format="json")
        self.user = User.objects.get(pk=response.json()['id'])

    def test_admin_create_user(self):
        """
        Ensure admin can create a non admin user
        """
        self.client.force_authenticate(self.superuser)

        self.assertTrue(self.superuser.is_superuser)

        url = reverse("api:users-list")
        data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "abcd1234",
            "first_name": "test2",
            "last_name": "user"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(username=response.json()["username"])
        self.assertFalse(new_user.is_superuser)

    def test_non_admin_cannot_create_user(self):
        """
        Ensure non admin user is not allowed to create a non admin user
        """
        self.client.force_authenticate(self.superuser)

        url = reverse("api:users-list")
        data_1 = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "abcd1234",
            "first_name": "test2",
            "last_name": "user"
        }
        response = self.client.post(url, data_1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(username=response.json()["username"])

        # new_user login
        self.client.force_authenticate(new_user)

        data_2 = {
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password": "abcd1234",
            "first_name": "test3",
            "last_name": "user"
        }
        response = self.client.post(url, data_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_created_along_with_user(self):
        self.client.force_authenticate(self.superuser)

        self.assertTrue(self.superuser.is_superuser)

        url = reverse("api:users-list")
        data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "abcd1234",
            "first_name": "test2",
            "last_name": "user"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(username=response.json()["username"])
        self.assertTrue(new_user.profile)

    def test_retrieve_user_by_superuser(self):
        self.client.force_authenticate(self.superuser)
        url = reverse("api:users-detail", args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_by_non_superuser(self):
        self.client.force_authenticate(self.user)
        url = reverse("api:users-detail", args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_by_non_superuser(self):
        self.client.force_authenticate(self.user)
        url = reverse("api:users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_partial_update_by_superuser(self):
        self.client.force_authenticate(self.superuser)
        url = reverse("api:users-detail", args=(self.user.id,))
        data = {
            "password": "abcd12345",
            "first_name": "testupdated",
            "last_name": "userupdated"
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], data["first_name"])
        self.assertEqual(response.json()['last_name'], data["last_name"])

    def test_user_destroy_by_superuser(self):
        self.client.force_authenticate(self.superuser)
        url = reverse("api:users-detail", args=(self.user.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(pk=self.user.id).exists())


class ProfileAPITest(APITestCase):
    def setUp(self) -> None:
        superuser = User.objects.create_superuser("iamsuper", "super@circle.com", "admin123")
        self.client.force_authenticate(superuser)
        url = reverse("api:users-list")
        data_1 = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "abcd1234",
            "first_name": "test",
            "last_name": "user"
        }
        response = self.client.post(url, data_1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(username=response.json()["username"])
        self.profile = new_user.profile
        self.client.force_authenticate(new_user)

    def test_profile_list(self):
        url = reverse("api:profiles-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_retrieve(self):
        url = reverse("api:profiles-detail", args=(self.profile.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
