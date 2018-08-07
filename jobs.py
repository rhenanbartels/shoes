import argparse

from datetime import datetime

from client.instagram import login
from commands import update_users, search_feed_media, search_stories


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--command", help="Choose command to run")


if __name__ == "__main__":
    api = login()
    db_users = None
    db_media = None

    args = parser.parse_args()
    if args.command == 'update-followers':
        followers = api.getTotalFollowers(api.username_id)
        update_users(api, db_users, orgin='follower')

    elif args.command == 'update-followings':
        followings = api.getTotalFollowings(api.username_id)
        update_users(api, db_users, orgin='following')

    elif args.command == 'update-media':
        followers = db_users.find(
                {'origin': 'follower'}
        ).limit(50).sort("last_visited")

        followings = db_users.find(
                {'origin': 'following'}
        ).limit(50).sort("last_visited")

        users = followers + followings
        for user in users:
            search_feed_media(api, db_media, user)
            search_stories(api, db_media, user)

            now = datetime.utcnow().timestamp()
            user['last_visited'] = now
            db_users.upddate_one(
                    {'pk': user['pk'], 'origin': user['origin']},
                    {"$set": user}, upsert=True
            )
