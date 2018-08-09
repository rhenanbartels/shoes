from django.http import JsonResponse
from django.views import View

from core.models import client


class UsersView(View):
    def get(self, request, *args, **kwargs):
        db_users = client.shoes.users
        users = list(db_users.find({}, {'_id': 0}))
        return JsonResponse(users, safe=False)


class FeedView(View):
    def get(self, request, *args, **kwargs):
        db_users = client.shoes.media
        users = list(db_users.find({}, {'_id': 0}))
        return JsonResponse(users, safe=False)
