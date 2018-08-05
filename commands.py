import math

from copy import deepcopy
from datetime import datetime

from client_google_vision import vision_api
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


def search_feed_media(api, db_collection, user, delta=1440,
                      percent_non_target=0.1):
    medias = get_recent_media(api, user, delta)
    # Number of non target images to be saved
    # Save at least one non target image
    n_non_target = max(math.floor(len(medias) * percent_non_target), 1)

    count = 0
    for media in medias:
        # Check if media contains a photo
        if 'image_versions2' in media:
            is_target = vision_api()
            media['source'] = 'feed'
            if is_target:
                media['is_target'] = is_target
                db_collection.insert_one(media)
            elif count < n_non_target:
                media['is_target'] = is_target
                db_collection.insert_one(media)
                count += 1


def search_stories(api, db_collection, user, percent_non_target=0.1):
    stories = get_stories(api, user)
    n_non_target = max(math.floor(len(stories) * percent_non_target), 1)

    count = 0
    for storie in stories['items']:
        if storie['media_type'] == 1:
            is_target = vision_api()
            storie['source'] = 'story'
            if is_target:
                storie['is_target'] = is_target
                db_collection.insert_one(storie)
            elif count < n_non_target:
                storie['is_target'] = is_target
                db_collection.insert_one(storie)
