from unittest import mock

from commands import update_users


def test_save_followings():
    followings = [
            {'username': 'username1', 'pk': 1234},
            {'username': 'username2', 'pk': 5678}
    ]

    document_mock = mock.MagicMock()

    update_users(document_mock, followings, origin='following')

    calls = [
            mock.call(
                {'pk': 1234},
                {'$set': {
                    'pk': 1234, 'username': 'username1', 'origin': 'following'
                }
                },
                upsert=True),
            mock.call(
                {'pk': 5678},
                {'$set': {
                    'pk': 5678, 'username': 'username2', 'origin': 'following'
                }
                },
                upsert=True)
    ]
    document_mock.find_one_and_update.assert_has_calls(calls)


def test_save_followers():
    followers = [
            {'username': 'username1', 'pk': 1234},
            {'username': 'username2', 'pk': 5678}
    ]

    document_mock = mock.MagicMock()

    update_users(document_mock, followers, origin='follower')

    calls = [
            mock.call(
                {'pk': 1234},
                {'$set': {
                    'pk': 1234, 'username': 'username1', 'origin': 'follower'
                }
                },
                upsert=True),
            mock.call(
                {'pk': 5678},
                {'$set': {
                    'pk': 5678, 'username': 'username2', 'origin': 'follower'
                }
                },
                upsert=True)
    ]
    document_mock.find_one_and_update.assert_has_calls(calls)
