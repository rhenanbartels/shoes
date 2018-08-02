from copy import deepcopy

from unittest import mock

from commands import update_users, search_feed_media, search_stories
from fixtures import media_resp_1, media_resp_2, storie_resp_1, storie_resp_2

# TODO: document -> collection

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
    collection_mock.find_one_and_update.assert_has_calls(calls)


@mock.patch('commands.visual_api')
@mock.patch('commands.get_recent_media')
def test_save_media(_get_recent_media, _visual_api):
    user = {'username': 'username1', 'pk': 1234},

    _visual_api.side_effect = [True, False]

    expected_media = deepcopy(media_resp_1)
    expected_media[0]['source'] = 'feed'

    _get_recent_media.side_effect = [media_resp_1, media_resp_2]
    api_mock = mock.MagicMock()

    collection_mock = mock.MagicMock()

    search_feed_media(api_mock, collection_mock, user)

    _get_recent_media.assert_called_once_with(api_mock, user, 1440)
    collection_mock.insert_one.assert_called_once_with(expected_media[0])


@mock.patch('commands.visual_api')
@mock.patch('commands.get_recent_media')
def test_save_media_only_with_shoes(_get_recent_media, _visual_api):
    user = {'username': 'username1', 'pk': 1234}

    _visual_api.side_effect = [True, False]

    expected_media_1 = deepcopy(media_resp_1)
    expected_media_1[0]['source'] = 'feed'
    expected_media_1[1]['source'] = 'feed'

    _get_recent_media.side_effect = [media_resp_1, media_resp_2]
    api_mock = mock.MagicMock()
    media_calls = [mock.call(api_mock, user, 1440)]

    collection_mock = mock.MagicMock()

    search_feed_media(api_mock, collection_mock, user)

    _get_recent_media.assert_has_calls(media_calls)
    collection_mock.insert_one.assert_called_once_with(expected_media_1[0])


@mock.patch('commands.visual_api')
@mock.patch('commands.get_stories')
def test_save_media_from_stories(_get_stories, _visual_api):
    user = {'username': 'username1', 'pk': 1234}

    api_mock = mock.MagicMock()
    _get_stories.side_effect = [storie_resp_1, storie_resp_2]
    collection_mock = mock.MagicMock()

    expected_storie = deepcopy(storie_resp_1)
    expected_storie['items'][0]['source'] = 'story'

    search_stories(api_mock, collection_mock, user)

    _get_stories.assert_called_once_with(api_mock, user)
    collection_mock.insert_one.assert_called_once_with(
            expected_storie['items'][0]
    )
