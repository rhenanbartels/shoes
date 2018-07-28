from unittest import mock

from freezegun import freeze_time

from client import get_recent_media
from fixtures import followers


@freeze_time('2018-07-18 12:00:00')
def test_get_recent_media():
    api_mock = mock.MagicMock()
    api_mock.getTotalUserFeed.side_effect = [
            [{'media': 'media1'}],
            [{'media': 'media2'}]
    ]

    media = get_recent_media(api_mock, followers)

    expected_calls = [
        mock.call(1234, minTimestamp=1531924200.0),
        mock.call(5678, minTimestamp=1531924200.0)
    ]
    actual_calls = api_mock.getTotalUserFeed.call_args_list

    assert expected_calls[0] in actual_calls
    assert expected_calls[1] in actual_calls
    assert media == [{'media': 'media1'}, {'media': 'media2'}]
