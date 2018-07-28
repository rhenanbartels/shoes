from datetime import datetime, timedelta

from decouple import config
from InstagramAPI import InstagramAPI


def login():
    username = config('USERNAME')
    passwd = config('PASSWD')
    api = InstagramAPI(username, passwd)
    api.login()
    return api


def get_recent_media(api, user, delta=30):
    last_30_min = (
            datetime.utcnow() - timedelta(minutes=delta)
    ).timestamp()
    try:
        media = api.getTotalUserFeed(user['pk'], minTimestamp=int(last_30_min))
    except KeyError:
        media = []

    return media
