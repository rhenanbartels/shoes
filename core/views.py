import re

from datetime import datetime, timedelta

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

        media = []

        page_num = int(request.GET.get('page', 1))

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        location = request.GET.get('location')
        hashtags = request.GET.get('hashtags')
        username = request.GET.get('username')

        db_media = client.shoes.media
        if start_date and end_date:
            media = _date_search(db_media, start_date, end_date, page_num,
                                 N_MEDIA_PAGE)
        elif location:
            media = _location_search(db_media, location, page_num,
                                     N_MEDIA_PAGE)
        elif hashtags:
            media = _hashtags_search(db_media, hashtags, page_num,
                                     N_MEDIA_PAGE)
        elif username:
            media = _username_search(db_media, hashtags, page_num,
                                     N_MEDIA_PAGE)

        return JsonResponse(media, safe=False)


def _date_search(db_media, start_date, end_date, page_num, n_media):
    start_date = int(start_date)
    end_date = _date_time_delta(int(end_date))
    return paginate(
            db_media.find({'taken_at': {'$gt': start_date,
                           '$lte': end_date}}, {'_id': 0}),
            page_num,
            n_media
    )


def _location_search(db_media, location, page_num, n_media):
    loc_pattern = re.compile(location, re.IGNORECASE)
    return paginate(db_media.find(
            {'$and': [
                {'source': 'feed'},
                {'location.name': loc_pattern}
            ]}, {'_id': 0}),
            page_num,
            n_media
    )


def _hashtags_search(db_media, hashtags, page_num, n_media):
    tags_pattern = re.compile(hashtags, re.IGNORECASE)
    return paginate(db_media.find(
        {'caption.text': tags_pattern},
        {'_id': 0}),
        page_num,
        n_media
    )


def _username_search(db_media, username, page_num, n_media):
    username_pattern = re.compile(username, re.IGNORECASE)
    return paginate(db_media.find(
        {'user.username': username_pattern},
        {'_id': 0}),
        page_num,
        n_media
    )


def _date_time_delta(end_date):
    end = datetime.fromtimestamp(end_date)
    return (end + timedelta(days=1)).timestamp()
