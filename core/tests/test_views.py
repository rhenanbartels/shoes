from django.urls import reverse
from django.test import TestCase


class UsersView(TestCase):
    def test_get_users(self, _client):
        url = reverse('users')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)


class FeedView(TestCase):
    def test_get_feed(self):
        url = reverse('feed')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
