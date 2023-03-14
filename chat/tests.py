from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from chat.models import ChatGroup


class ChatGroupAPITest(APITestCase):
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

        data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "abcd1234",
            "first_name": "test2",
            "last_name": "user"
        }
        response = self.client.post(url, data, format="json")

        self.user2 = User.objects.get(pk=response.json()['id'])

        self.client.force_authenticate(self.user)
        self.chat_group = ChatGroup.objects.create(name="testgroup")

    def test_chat_group_create(self):
        url = reverse("api:chat-groups-list")
        data = {
            "name": "group1",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_chat_group_retrieve(self):
        url = reverse("api:chat-groups-detail", args=(self.chat_group.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_group_list(self):
        url = reverse("api:chat-groups-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_group_destroy(self):
        url = reverse("api:chat-groups-detail", args=(self.chat_group.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_group_add_profile(self):
        url = reverse("api:chat-groups-add-profile", args=(self.chat_group.id,))

        data = {
            "profiles": [self.user.profile.id, self.user2.profile.id]
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_group_list_profiles(self):
        url = reverse("api:chat-groups-list-profiles", args=(self.chat_group.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_group_remove_profile(self):
        self.chat_group.profiles.add(self.user2.profile)

        url = reverse("api:chat-groups-remove-profile", args=(self.chat_group.id,))

        data = {
            'profile': self.user2.profile.id
        }
        response = self.client.delete(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MessageAPITest(APITestCase):
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

        data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "abcd1234",
            "first_name": "test2",
            "last_name": "user"
        }
        response = self.client.post(url, data, format="json")

        self.user2 = User.objects.get(pk=response.json()['id'])

        self.client.force_authenticate(self.user)
        self.chat_group = ChatGroup.objects.create(name="testgroup")

    def test_message_create(self):
        url = reverse("api:messages-list")
        data = {
            "content": "Hi there everyone!",
            "chat_group": self.chat_group.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_message_retrieve(self):
        url = reverse("api:messages-list")
        data = {
            "content": "Hi there everyone!",
            "chat_group": self.chat_group.id
        }
        response = self.client.post(url, data, format="json")
        url = reverse("api:messages-detail", args=(response.json()['id'],))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_list(self):
        url = reverse("api:messages-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_destroy(self):
        url = reverse("api:messages-list")
        data = {
            "content": "Hi there everyone!",
            "chat_group": self.chat_group.id
        }
        response = self.client.post(url, data, format="json")

        url = reverse("api:messages-detail", args=(response.json()['id'],))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_like(self):
        url = reverse("api:messages-list")
        data = {
            "content": "Hi there everyone!",
            "chat_group": self.chat_group.id
        }
        response = self.client.post(url, data, format="json")

        url = reverse("api:messages-like", args=(response.json()['id'], ))

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
