from decouple import config
from InstagramAPI import InstagramAPI


def login():
    username = config('USERNAME')
    passwd = config('PASSWD')
    api = InstagramAPI(username, passwd)
    api.login()
    return api
