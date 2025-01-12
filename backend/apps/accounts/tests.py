from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User


class AccountAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username='admin_user',
            email='admin@example.com',
            password='admin_password'
        )
        self.regular_user = User.objects.create_user(
            username='regular_user',
            email='regular@example.com',
            password='regular_password'
        )

    def test_create_user_as_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('user-list')

        data = {
            'username': 'john-doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'john_password'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.filter(username=data.get('username')).first()
        self.assertEqual(data.get('username'), user.username)
        self.assertEqual(data.get('first_name'), user.first_name)
        self.assertEqual(data.get('last_name'), user.last_name)
        self.assertEqual(data.get('email'), user.email)

    def test_create_user_as_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('user-list')

        data = {
            'username': 'jane-doe',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'password': 'jane_password'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_anonymous(self) -> None:
        url = reverse('user-list')

        data = {
            'username': 'alice-smith',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'password': 'alice_password'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_as_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_get_all_users_as_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_as_anonymous(self) -> None:
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_a_user_as_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('user-detail', kwargs={'uuid': self.admin_user.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_user_as_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('user-detail', kwargs={'uuid': self.regular_user.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_a_user_as_anonymous(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('user-detail', kwargs={'uuid': self.regular_user.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('user-detail', kwargs={'uuid': self.admin_user.uuid})

        data = {
            'username': 'mike-brown',
            'first_name': 'Mike',
            'last_name': 'Brown',
            'email': 'mike.brown@example.com'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.filter(uuid=self.admin_user.uuid).first()
        self.assertEqual(data.get('username'), user.username)
        self.assertEqual(data.get('first_name'), user.first_name)
        self.assertEqual(data.get('last_name'), user.last_name)
        self.assertEqual(data.get('email'), user.email)

    def test_update_user_as_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('user-detail', kwargs={'uuid': self.regular_user.uuid})

        data = {
            'username': 'emily-wilson',
            'first_name': 'Emily',
            'last_name': 'Wilson',
            'email': 'emily.wilson@example.com'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_anonymous(self) -> None:
        url = reverse('user-detail', kwargs={'uuid': self.regular_user.uuid})

        data = {
            'username': 'chris-taylor',
            'first_name': 'Chris',
            'last_name': 'Taylor',
            'email': 'chris.taylor@example.com'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_as_admin(self) -> None:
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('user-detail', kwargs={'uuid': self.admin_user.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user = User.objects.filter(uuid=self.admin_user.uuid).first()
        self.assertIsNone(user)

    def test_delete_user_as_non_admin(self) -> None:
        self.client.login(username='regular_user', password='regular_password')
        url = reverse('user-detail', kwargs={'uuid': self.regular_user.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_as_anonymous(self) -> None:
        url = reverse('user-detail', kwargs={'uuid': self.regular_user.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
