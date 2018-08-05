import base64

from unittest import mock

import responses

from decouple import config

from client_google_vision import find_keywords, get_identified_labels
from fixtures import vision_api_non_target, vision_api_target


def test_find_target_keywords():
    not_target = find_keywords(vision_api_non_target['responses'][0])
    target = find_keywords(vision_api_target['responses'][0])

    assert not_target is False
    assert target is True


@responses.activate
def test_get_google_vision_api_response():
    api_version = config('VISION_API_VERSION')
    token = config("VISION_TOKEN")

    with open('test_images/vision_test_image.jpg', 'rb') as image:
        image_content = image.read()
        base64_image = base64.b64encode(image_content).decode()

    responses.add(
            responses.POST,
            "https://vision.googleapis.com/{api_version}/images:annotate?"
            "key={token}".format(api_version=api_version, token=token),
            json=vision_api_non_target,
            status=200
            )

    labels = get_identified_labels(base64_image)

    assert labels == vision_api_non_target['responses'][0]


@mock.patch('client_google_vision.get_identified_labels')
@mock.patch('client_google_vision.requests.get')
def test_vision_api_use(_get, _get_labels):
    pass
