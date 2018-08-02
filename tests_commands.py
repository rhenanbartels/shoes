from copy import deepcopy

from unittest import mock

from commands import update_users, search_feed_media, search_stories
from fixtures import media_resp_1, media_resp_2, storie_resp_1, storie_resp_2


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


@mock.patch('commands.visual_api')
@mock.patch('commands.get_recent_media')
def test_save_media(_get_recent_media, _visual_api):
    user1 = {'username': 'username1', 'pk': 1234},
    user2 = {'username': 'username2', 'pk': 5678}
    followers = [user1, user2]

    _visual_api.side_effect = [True, True, True, True]

    expected_media_1 = deepcopy(media_resp_1)
    expected_media_2 = deepcopy(media_resp_2)
    expected_media_1[0]['source'] = 'feed'
    expected_media_2[0]['source'] = 'feed'
    expected_media_2[1]['source'] = 'feed'

    _get_recent_media.side_effect = [media_resp_1, media_resp_2]
    api_mock = mock.MagicMock()
    media_calls = [mock.call(api_mock, user1, 1440),
                   mock.call(api_mock, user2, 1440)]
    document_db_calls = [
            mock.call(expected_media_1[0]),
            mock.call(expected_media_2[0]),
            mock.call(expected_media_2[1])
    ]

    document_mock = mock.MagicMock()

    search_feed_media(api_mock, document_mock, followers)

    _get_recent_media.assert_has_calls(media_calls)
    document_mock.insert_one.assert_has_calls(document_db_calls)


@mock.patch('commands.visual_api')
@mock.patch('commands.get_recent_media')
def test_save_media_only_with_shoes(_get_recent_media, _visual_api):
    users = [{'username': 'username1', 'pk': 1234}]

    _visual_api.side_effect = [True, False]

    expected_media_1 = deepcopy(media_resp_1)
    expected_media_1[0]['source'] = 'feed'
    expected_media_1[1]['source'] = 'feed'

    _get_recent_media.side_effect = [media_resp_1, media_resp_2]
    api_mock = mock.MagicMock()
    media_calls = [mock.call(api_mock, users[0], 1440)]

    document_mock = mock.MagicMock()

    search_feed_media(api_mock, document_mock, users)

    _get_recent_media.assert_has_calls(media_calls)
    document_mock.insert_one.assert_called_once_with(expected_media_1[0])


@mock.patch('commands.visual_api')
@mock.patch('commands.get_stories')
def test_save_media_from_stories(_get_stories, _visual_api):
    users = [
        {'username': 'username1', 'pk': 1234},
        {'username': 'username1', 'pk': 5678}
    ]

    api_mock = mock.MagicMock()
    _get_stories.side_effect = [storie_resp_1, storie_resp_2]
    document_mock = mock.MagicMock()

    expected_storie_1 = deepcopy(storie_resp_1)
    expected_storie_2 = deepcopy(storie_resp_2)
    expected_storie_1['items'][0]['source'] = 'story'
    expected_storie_2['items'][0]['source'] = 'story'
    expected_storie_2['items'][1]['source'] = 'story'

    stories_calls = [
            mock.call(api_mock, users[0]),
            mock.call(api_mock, users[1])
    ]
    document_db_calls = [
            mock.call(expected_storie_1['items'][0]),
            mock.call(expected_storie_2['items'][0]),
            mock.call(expected_storie_2['items'][1])
    ]

    search_stories(api_mock, document_mock, users)

    _get_stories.assert_has_calls(stories_calls)
    document_mock.insert_one.assert_has_calls(document_db_calls)
