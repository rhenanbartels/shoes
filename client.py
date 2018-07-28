from datetime import datetime, timedelta

from decouple import config
from InstagramAPI import InstagramAPI


def login():
    username = config('USERNAME')
    passwd = config('PASSWD')
    api = InstagramAPI(username, passwd)
    api.login()
    return api


def get_recent_media(api, users):
    media = []
    last_30_min = (
            datetime.utcnow() - timedelta(minutes=30)
    ).timestamp()
    for user in users:
        media.extend(
            api.getTotalUserFeed(user['pk'], minTimestamp=last_30_min)
        )

    return media
