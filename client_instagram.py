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
    time_delta = (
            datetime.utcnow() - timedelta(minutes=delta)
    ).timestamp()
    try:
        media = api.getTotalUserFeed(user['pk'], minTimestamp=int(time_delta))
    except KeyError:
        media = []

    return media


def get_stories(api, user):
    api.SendRequest('feed/user/' + str(user['pk']) + '/reel_media/')
    return api.LastJson
