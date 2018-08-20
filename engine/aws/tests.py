from unittest import mock

from decouple import config

from aws.client import login, send_image_aws


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


def test_send_image():
    client_mock = mock.MagicMock()
    img_mock = mock.MagicMock()
    img_name = 'test_image'
    aws_url = '{bucket}.{endpoint}/imagens/foto/shoes/{name}.jpg'.format(
            bucket='https://' + config('AWS_BUCKET_NAME'),
            endpoint=config('AWS_ENDPOINT_URL').replace('https://', ''),
            name=img_name
    )
    aws_name = 'imagens/foto/shoes/{name}.jpg'.format(
            name=img_name
    )

    image_url = send_image_aws(client_mock, img_mock, img_name)

    client_mock.upload_fileobj.assert_called_once_with(
            img_mock,
            config('AWS_BUCKET_NAME'),
            aws_name,
            ExtraArgs={"ContentType": "image/jpeg", "ACL": "public-read"}
    )

    assert image_url == aws_url
