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
            image_url = media['image_versions2']['candidates'][0]['url']
            is_target, image_base64 = vision_api(image_url)
            media['source'] = 'feed'
            media['image_base64'] = image_base64
            id_media = media.pop('id')
            if is_target:
                media['is_target'] = is_target
                db_collection.update_one(
                        {'id': id_media},
                        {'$set': media},
                        upsert=True
                )
            elif count < n_non_target:
                media['is_target'] = is_target
                db_collection.update_one(
                        {'id': id_media},
                        {'$set': media},
                        upsert=True
                )
                count += 1


def search_stories(api, db_collection, user, percent_non_target=0.1):
    stories = get_stories(api, user)
    n_non_target = max(math.floor(len(stories) * percent_non_target), 1)

    count = 0
    for storie in stories['items']:
        if storie['media_type'] == 1:
            image_url = storie['image_versions2']['candidates'][0]['url']
            is_target, image_base64 = vision_api(image_url)
            storie['source'] = 'story'
            storie['image_base64'] = image_base64
            storie_id = storie.pop('id')
            if is_target:
                storie['is_target'] = is_target
                db_collection.update_one(
                        {'id': storie_id},
                        {'$set': storie},
                        upsert=True
                )
            elif count < n_non_target:
                storie['is_target'] = is_target
                db_collection.update_one(
                        {'id': storie_id},
                        {'$set': storie},
                        upsert=True
                )
                count += 1
