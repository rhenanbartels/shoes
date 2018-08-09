from django.urls import reverse
from django.test import TestCase


class UsersView(TestCase):
    def test_get_users(self):
        url = reverse('users')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
