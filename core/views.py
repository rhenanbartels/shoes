from decouple import config
from django.http import JsonResponse
from django.views import View
from pymongo import MongoClient


class UsersView(View):
    def get(self, request, *args, **kwargs):
        client = MongoClient(
                config('MONGO_ADDR'),
                config('MONGO_PORT', cast=int)
        )
        db_users = client.shoes.users
        users = list(db_users.find({}, {'_id': 0}))
        return JsonResponse(users, safe=False)


class FeedView(View):
    def get(self, request, *args, **kwargs):
        client = MongoClient(
                config('MONGO_ADDR'),
                config('MONGO_PORT', cast=int)
        )
        db_users = client.shoes.media
        users = list(db_users.find({}, {'_id': 0}))
        return JsonResponse(users, safe=False)
