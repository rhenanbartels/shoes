from unittest import mock

from freezegun import freeze_time

from engine.client_instagram import get_recent_media, get_stories
from engine.tests.fixtures import followers


@freeze_time('2018-07-18 12:00:00')
def test_get_recent_media():
    api_mock = mock.MagicMock()
    api_mock.getTotalUserFeed.return_value = [
            {'media': 'media1'},
    ]

    media = get_recent_media(api_mock, followers[0], delta=1440)

    api_mock.getTotalUserFeed.assert_called_once_with(
            1234,
            minTimestamp=1531839600,
    )
    assert media == [{'media': 'media1'}]


def test_get_stories():
    api_mock = mock.MagicMock()
    api_mock.LastJson = {'items': [1, 2, 3]}

    stories = get_stories(api_mock, followers[0])

    api_mock.SendRequest.assert_called_once_with(
            'feed/user/1234/reel_media/'
    )
    assert stories == {'items': [1, 2, 3]}


# https://github.com/Hironsan/google-vision-sampler
