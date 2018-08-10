import argparse

from datetime import datetime

from decouple import config
from pymongo import MongoClient

from client_instagram import login
from commands import update_users, search_feed_media, search_stories


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", help="Choose command to run")

    api = login()
    client = MongoClient(
            host=config('MONGO_ADDR'),
            port=config('MONGO_PORT', cast=int),
            username=config('MONGO_USER'),
            password=config('MONGO_PWD'),
            authSource=config('MONGO_AUTH_DB')
    )
    db_users = client.shoes.users
    db_media = client.shoes.media

    arguments = parser.parse_args()
    if arguments.command == 'update-followers':
        followers = api.getTotalFollowers(api.username_id)
        update_users(db_users, followers, origin='follower')

    elif arguments.command == 'update-followings':
        followings = api.getTotalFollowings(api.username_id)
        update_users(db_users, followings, origin='following')

    elif arguments.command == 'update-media':
        followers = db_users.find(
                {'origin': 'follower'}
        ).limit(50).sort("last_visited")

        followings = db_users.find(
                {'origin': 'following'}
        ).limit(50).sort("last_visited")

        users = list(followers) + list(followings)
        for user in users:
            search_feed_media(api, db_media, user)
            search_stories(api, db_media, user)

            now = datetime.utcnow().timestamp()
            user['last_visited'] = now
            db_users.update_one(
                    {'pk': user['pk'], 'origin': user['origin']},
                    {"$set": user}, upsert=True
            )
