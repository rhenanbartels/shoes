from unittest import mock

from freezegun import freeze_time

from client import get_recent_media
from fixtures import followers


@freeze_time('2018-07-18 12:00:00')
def test_get_recent_media():
    api_mock = mock.MagicMock()
    api_mock.getTotalUserFeed.return_value = [
            {'media': 'media1'},
    ]

    media = get_recent_media(api_mock, followers[0], delta=30)

    api_mock.getTotalUserFeed.assert_called_once_with(
            1234,
            minTimestamp=1531924200,
    )
    assert media == [{'media': 'media1'}]
