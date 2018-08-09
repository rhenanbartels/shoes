from django.http import JsonResponse
from django.views import View

from core.models import client


N_USER_PAGE = 2
N_MEDIA_PAGE = 2


def paginate(collection, page, n_elements):
    start = (page - 1) * n_elements
    return list(collection.find({}, {'_id': 0}).skip(start).limit(n_elements))


class UsersView(View):
    def get(self, request, *args, **kwargs):
        page_num = int(request.GET.get('page', 1))

        db_users = client.shoes.users
        users = paginate(db_users, page_num, N_USER_PAGE)

        return JsonResponse(users, safe=False)


class FeedView(View):
    def get(self, request, *args, **kwargs):
        page_num = int(request.GET.get('page', 1))

        db_media = client.shoes.media
        media = paginate(db_media, page_num, N_MEDIA_PAGE)

        return JsonResponse(media, safe=False)
