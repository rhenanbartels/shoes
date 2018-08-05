from copy import deepcopy

from unittest import mock

from commands import update_users, search_feed_media, search_stories
from fixtures import media_resp_1, media_resp_2, storie_resp_1, storie_resp_2
from freezegun import freeze_time


@freeze_time('2018-08-02 12:00:00')
def test_save_followings():
    followings = [
            {'username': 'username1', 'pk': 1234},
            {'username': 'username2', 'pk': 5678}
    ]

    collection_mock = mock.MagicMock()

    update_users(collection_mock, followings, origin='following')

    calls = [
            mock.call(
                {'pk': 1234, 'origin': 'following'},
                {'$set': {
                    'username': 'username1', 'last_visited': 1533222000
                }
                },
                upsert=True),
            mock.call(
                {'pk': 5678, 'origin': 'following'},
                {'$set': {
                    'username': 'username2', 'last_visited': 1533222000
                }
                },
                upsert=True)
    ]
    collection_mock.update_one.assert_has_calls(calls)
    assert followings[0] == {'username': 'username1', 'pk': 1234}
    assert followings[1] == {'username': 'username2', 'pk': 5678}


@freeze_time('2018-08-02 12:00:00')
def test_save_followers():
    followers = [
            {'username': 'username1', 'pk': 1234},
            {'username': 'username2', 'pk': 5678}
    ]

    collection_mock = mock.MagicMock()

    update_users(collection_mock, followers, origin='follower')

    calls = [
            mock.call(
                {'pk': 1234, 'origin': 'follower'},
                {'$set': {
                    'username': 'username1', 'last_visited': 1533222000
                }
                },
                upsert=True),
            mock.call(
                {'pk': 5678, 'origin': 'follower'},
                {'$set': {
                    'username': 'username2', 'last_visited': 1533222000
                }
                },
                upsert=True)
    ]
    collection_mock.update_one.assert_has_calls(calls)
    assert followers[0] == {'username': 'username1', 'pk': 1234}
    assert followers[1] == {'username': 'username2', 'pk': 5678}


@mock.patch('commands.visual_api')
@mock.patch('commands.get_recent_media')
def test_save_media(_get_recent_media, _visual_api):
    user = {'username': 'username1', 'pk': 1234},

    _visual_api.side_effect = [True, False]

    expected_media = deepcopy(media_resp_1)
    expected_media[0]['source'] = 'feed'
    expected_media[0]['is_target'] = True

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
    expected_media_1[0]['is_target'] = True

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

    _visual_api.return_value = True
    api_mock = mock.MagicMock()
    _get_stories.side_effect = [storie_resp_1, storie_resp_2]
    collection_mock = mock.MagicMock()

    expected_storie = deepcopy(storie_resp_1)
    expected_storie['items'][0]['source'] = 'story'
    expected_storie['items'][0]['is_target'] = True

    search_stories(api_mock, collection_mock, user)

    _get_stories.assert_called_once_with(api_mock, user)
    collection_mock.insert_one.assert_called_once_with(
            expected_storie['items'][0]
    )


@mock.patch('commands.visual_api')
@mock.patch('commands.get_recent_media')
def test_save_samples_of_non_target_images_from_feed(
        _get_recent_media, _visual_api):

    user = {'username': 'username1', 'pk': 1234}

    # In this test case all images are non target
    _visual_api.side_effect = [False is True for i in range(10)]
    collection_mock = mock.MagicMock()
    _get_recent_media.return_value = [
            {'non_image': None},
            {'image_versions2': 'image_0'},
            {'non_image': None},
            {'non_image': None},
            {'non_image': None},
            {'image_versions2': 'image_1'},
    ]

    api_mock = mock.MagicMock()
    search_feed_media(api_mock, collection_mock, user)

    collection_mock.insert_one.assert_called_once_with(
            {
             'image_versions2': 'image_0',
             'source': 'feed',
             'is_target': False
            }
    )


@mock.patch('commands.visual_api')
@mock.patch('commands.get_stories')
def test_save_samples_of_non_target_images_from_stories(
        _get_stories, _visual_api):

    user = {'username': 'username1', 'pk': 1234}

    # In this test case all images are non target
    _visual_api.side_effect = [False is True for i in range(10)]
    collection_mock = mock.MagicMock()
    _get_stories.return_value = {
            'items':
            [{'media_type': 2},
             {'media_type': 1, 'image_versions2': 'image_0'},
             {'media_type': 2},
             {'media_type': 2},
             {'media_type': 2},
             {'media_type': '1', 'image_versions2': 'image_1'}]
            }

    api_mock = mock.MagicMock()
    search_stories(api_mock, collection_mock, user)

    collection_mock.insert_one.assert_called_once_with(
            {
             'image_versions2': 'image_0',
             'source': 'story',
             'is_target': False,
             'media_type': 1
            }
    )
