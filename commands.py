from copy import deepcopy
from datetime import datetime

from client_google_visual import visual_api
from client_instagram import get_recent_media, get_stories


def update_users(db_collection, users, origin):
    now = datetime.utcnow().timestamp()
    users = deepcopy(users)
    for user in users:
        pk = user.pop('pk')
        user['last_visited'] = now
        db_collection.update_one(
                {'pk': pk, 'origin': origin},
                {'$set': user}, upsert=True
        )


def search_feed_media(api, db_collection, user, delta=1440):
    medias = get_recent_media(api, user, delta)
    for media in medias:
        # Check if media contains a photo
        if 'image_versions2' in media:
            is_target = visual_api()
            if is_target:
                media['source'] = 'feed'
                media['is_target'] = is_target
                db_collection.insert_one(media)


def search_stories(api, db_collection, user):
    stories = get_stories(api, user)
    for storie in stories['items']:
        if storie['media_type'] == 1:
            is_target = visual_api()
            if is_target:
                storie['source'] = 'story'
                storie['is_target'] = is_target
                db_collection.insert_one(storie)
