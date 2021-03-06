import base64
import responses

from io import BytesIO
from unittest import mock

from decouple import config
from PIL import Image

from engine.client_google_vision import (find_keywords,
                                         get_identified_labels,
                                         crop_image,
                                         vision_api)
from engine.tests.fixtures import vision_api_non_target, vision_api_target


def test_find_target_keywords():
    not_target = find_keywords(vision_api_non_target['responses'][0])
    target = find_keywords(vision_api_target['responses'][0])

    assert not_target is False
    assert target is True


@responses.activate
def test_get_google_vision_api_response():
    api_version = config('VISION_API_VERSION')
    token = config("VISION_TOKEN")

    with open('engine/tests/test_images/vision_test_image.jpg', 'rb') as image:
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
    with open('engine/tests/test_images/vision_test_image.jpg', 'rb') as image:
        img = base64.b64encode(image.read()).decode()
        cropped_img = crop_image(img, prop=(0.5, 1.0))
        cropped_img_pil = Image.open(BytesIO(base64.b64decode(cropped_img)))

        expected_height = 427
        expected_width = 1280

        assert cropped_img_pil.height == expected_height
        assert cropped_img_pil.width == expected_width


@mock.patch('engine.client_google_vision.BytesIO', return_value='img_obj')
@mock.patch('engine.client_google_vision.get_identified_labels')
@mock.patch('engine.client_google_vision.crop_image',
            return_value='cropped')
@mock.patch('engine.client_google_vision._prepare_image',
            return_value='prepared')
@mock.patch('engine.client_google_vision.requests.get')
def test_vision_api_pipeline(_get, _prepare_image, _crop_image, _get_labels,
                             _bytes_io):
    _get_labels.return_value = {
            'labelAnnotations': [{'description': 'shoe'}]
    }
    content_mock = mock.MagicMock()
    content_mock.content = 'image_content'
    _get.return_value = content_mock

    is_target, b64_img = vision_api('image_url')

    _get.assert_called_once_with('image_url')
    _prepare_image.assert_called_once_with(content_mock)
    _crop_image.assert_called_once_with('prepared', (0, 1.0))
    _get_labels.assert_called_once_with('cropped')
    _bytes_io.assert_called_once_with('image_content')
    assert is_target is True
    assert b64_img == 'img_obj'


@mock.patch('engine.client_google_vision.BytesIO', return_value='img_obj')
@mock.patch('engine.client_google_vision.get_identified_labels')
@mock.patch('engine.client_google_vision.crop_image',
            return_value='cropped')
@mock.patch('engine.client_google_vision._prepare_image',
            return_value='prepared')
@mock.patch('engine.client_google_vision.requests.get')
def test_vision_api_pipeline_false_response(_get, _prepare_image, _crop_image,
                                            _get_labels, _bytes_io):

    response_mock = mock.MagicMock()
    response_mock.content = 'response content'
    _get.return_value = response_mock
    _get_labels.return_value = {
            'labelAnnotations': [{'description': 'not_target'}]
    }

    is_target, img_obj = vision_api('image_url')
    crop_image_calls = [
            mock.call('prepared', (0.0, 1.0)),
            mock.call('prepared', (0.5, 1.0)),
            mock.call('prepared', (0.75, 1.0)),
            mock.call('prepared', (0.5, 0.75))
    ]
    get_labels_calls = [mock.call('cropped') for i in range(3)]

    _get.assert_called_once_with('image_url')
    _prepare_image.assert_called_once_with(response_mock)
    _bytes_io.assert_called_once_with('response content')
    _crop_image.assert_has_calls(crop_image_calls)
    _get_labels.assert_has_calls(get_labels_calls)
    assert is_target is False
    assert img_obj is 'img_obj'


@mock.patch('engine.client_google_vision.BytesIO', return_value='img_obj')
@mock.patch('engine.client_google_vision.crop_image',
            return_value='cropped')
@mock.patch('engine.client_google_vision.get_identified_labels')
@mock.patch('engine.client_google_vision._prepare_image',
            return_value='prepared')
@mock.patch('engine.client_google_vision.requests.get')
def test_vision_api_pipeline_with_half_img(_get, _prepare_image, _get_labels,
                                           _crop_image, _bytes_io):

    response_mock = mock.MagicMock()
    response_mock.content = 'response content'

    _get.return_value = response_mock
    _get_labels.side_effect = [
            {'labelAnnotations': [{'description': 'not shoe'}]},
            {'labelAnnotations': [{'description': 'shoe'}]}
    ]

    is_target, img_obj = vision_api('image_url')

    get_labels_calls = [mock.call('prepared'), mock.call('cropped')]
    crop_image_calls = [mock.call('prepared', (0.0, 1.0)),
                        mock.call('prepared', (0.5, 1.0))]

    _get.assert_called_once_with('image_url')
    _bytes_io.assert_called_once_with('response content')
    _prepare_image.assert_called_once_with(response_mock)
    _get_labels.call_args_list == get_labels_calls
    _crop_image.assert_has_calls(crop_image_calls)
    assert is_target is True
    assert img_obj == 'img_obj'
