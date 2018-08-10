from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView

from core.models import client


N_USER_PAGE = 2
N_MEDIA_PAGE = 2


def paginate(query_cursor, page, n_elements):
    start = (page - 1) * n_elements
    return list(query_cursor.skip(start).limit(n_elements))


class IndexView(TemplateView):
    template_name = 'core/index.html'


class ApiUsersView(View):
    def get(self, request, *args, **kwargs):
        page_num = int(request.GET.get('page', 1))

        db_users = client.shoes.users
        cursor = db_users.find({}, {'_id': 0})
        users = paginate(cursor, page_num, N_USER_PAGE)

        return JsonResponse(users, safe=False)


class ApiFeedView(View):
    def get(self, request, *args, **kwargs):
        page_num = int(request.GET.get('page', 1))

        db_media = client.shoes.media
        cursor = db_media.find({}, {'_id': 0})
        media = paginate(cursor, page_num, N_MEDIA_PAGE)

        return JsonResponse(media, safe=False)
