from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from core.models import client


N_USER_PAGE = 2
N_MEDIA_PAGE = 2


class UsersView(View):
    def get(self, request, *args, **kwargs):
        page_num = int(request.GET.get('page', 1))

        db_users = client.shoes.users
        users = list(db_users.find({}, {'_id': 0}))

        paginator = Paginator(users, N_USER_PAGE)
        page = paginator.page(page_num)

        return JsonResponse(page.object_list, safe=False)


class FeedView(View):
    def get(self, request, *args, **kwargs):
        page_num = int(request.GET.get('page', 1))

        db_media = client.shoes.media
        media = list(db_media.find({}, {'_id': 0}))

        paginator = Paginator(media, N_MEDIA_PAGE)
        page = paginator.page(page_num)

        return JsonResponse(page.object_list, safe=False)
