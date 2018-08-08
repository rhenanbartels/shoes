import base64
import responses

from io import BytesIO
from unittest import mock

from decouple import config
from PIL import Image

from client_google_vision import (find_keywords,
                                  get_identified_labels,
                                  crop_image,
                                  vision_api)
from tests.fixtures import vision_api_non_target, vision_api_target


def test_find_target_keywords():
    not_target = find_keywords(vision_api_non_target['responses'][0])
    target = find_keywords(vision_api_target['responses'][0])

    assert not_target is False
    assert target is True


@responses.activate
def test_get_google_vision_api_response():
    api_version = config('VISION_API_VERSION')
    token = config("VISION_TOKEN")

    with open('tests/test_images/vision_test_image.jpg', 'rb') as image:
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


def test_crop_image():
    with open('tests/test_images/vision_test_image.jpg', 'rb') as image:
        img = image.read()
        cropped_img = crop_image(img, prop=0.5)
        cropped_img_pil = Image.open(BytesIO(base64.b64decode(cropped_img)))

        expected_height = 427
        expected_width = 1280

        assert cropped_img_pil.height == expected_height
        assert cropped_img_pil.width == expected_width


@mock.patch('client_google_vision.get_identified_labels')
@mock.patch('client_google_vision._prepare_image', return_value='prepared')
@mock.patch('client_google_vision.requests.get', return_value='response')
def test_vision_api_pipeline(_get, _prepare_image, _get_labels):
    _get_labels.return_value = {
            'labelAnnotations': [{'description': 'shoe'}]
    }

    is_target, _ = vision_api('image_url')

    _get.assert_called_once_with('image_url')
    _prepare_image.assert_called_once_with('response')
    _get_labels.assert_called_once_with('prepared')
    assert is_target is True


@mock.patch('client_google_vision.crop_image', return_value='cropped')
@mock.patch('client_google_vision.get_identified_labels')
@mock.patch('client_google_vision._prepare_image', return_value='prepared')
@mock.patch('client_google_vision.requests.get')
def test_vision_api_pipeline_with_half_img(_get, _prepare_image, _get_labels,
                                           _crop_image):

    response_mock = mock.MagicMock()
    response_mock.content = 'response content'

    _get.return_value = response_mock
    _get_labels.side_effect = [
            {'labelAnnotations': [{'description': 'not shoe'}]},
            {'labelAnnotations': [{'description': 'shoe'}]}
    ]

    is_target, _ = vision_api('image_url')

    get_labels_calls = [mock.call('prepared'), mock.call('cropped')]

    _get.assert_called_once_with('image_url')
    _prepare_image.assert_called_once_with(response_mock)
    _get_labels.call_args_list == get_labels_calls
    _crop_image.assert_called_once_with('response content')
    assert is_target is True
