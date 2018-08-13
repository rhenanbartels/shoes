from datetime import datetime, time_delta

from decouple import config

from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView

from core.models import client


N_USER_PAGE = config('N_USER_PAGE', cast=int)
N_MEDIA_PAGE = config('N_MEDIA_PAGE', cast=int)


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
        cursor = db_media.find({"is_target": True}, {'_id': 0})
        media = paginate(cursor, page_num, N_MEDIA_PAGE)

        return JsonResponse(media, safe=False)


class ApiSearchView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        location = request.GET.get('location')
        tags = request.GET.get('tags')

        db_media = client.shoes.media
        if start_date and end_date:
            start_date = int(start_date)
            end_date = _date_time_delta(int(end_date))
            media = db_media.find(
                    {'taken_at': {'$gt': start_date, '$lte': end_date}}
            )
            return JsonResponse(media, safe=False)
        elif location:
            media = db_media.find(
                    {'$and': [
                        {'source': 'feed'},
                        {'location.name': {'$regex': location}}
                    ]}
            )
            return JsonResponse(media, safe=False)
        elif tags:
            media = db_media.find(
                    {'$and': [
                        {'source': 'feed'},
                        {'caption.text': {'$regex': location}}
                    ]}
            )


def _date_time_delta(end_date):
    end = datetime.fromtimestamp(end_date)
    return (end + time_delta(days=1)).timestamp()
