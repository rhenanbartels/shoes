from unittest import mock

from decouple import config

from aws.client import login


@mock.patch('aws.client.Session')
def test_login(_session):
    session_mock = mock.MagicMock()
    client_mock = mock.MagicMock()
    session_mock.client.return_value = client_mock
    _session.return_value = session_mock

    client = login()

    _session.assert_called_once_with()
    session_mock.client.assert_called_once_with(
            's3',
            region_name=config('AWS_REGION_NAME'),
            endpoint_url=config('AWS_ENDPOINT_URL'),
            aws_access_key_id=config('AWS_ACCESS_ID'),
            aws_secret_access_key=config('AWS_SECRET_KEY')
    )
    assert client is client_mock
