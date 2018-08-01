from client_google_visual import visual_api
from client_instagram import get_recent_media


def update_users(db_document, users, origin):
    for user in users:
        pk = user['pk']
        user['origin'] = origin
        db_document.find_one_and_update(
                {'pk': pk}, {'$set': user}, upsert=True
        )


def search_media(api, db_document, users, source, delta=1440):
    for user in users:
        medias = get_recent_media(api, user, delta)
        for media in medias:
            # Check if media contains a photo
            if 'image_versions2' in media:
                is_target = visual_api()
                if is_target:
                    media['source'] = source
                    db_document.insert_one(media)
