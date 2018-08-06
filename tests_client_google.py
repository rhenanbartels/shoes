import base64
import responses

from io import BytesIO

from decouple import config
from PIL import Image

from client_google_vision import (find_keywords,
                                  get_identified_labels,
                                  crop_image)
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


def test_crop_image():
    with open('test_images/vision_test_image.jpg', 'rb') as image:
        img = image.read()
        cropped_img = crop_image(img, prop=0.5)
        cropped_img_pil = Image.open(BytesIO(base64.b64decode(cropped_img)))

        expected_height = 427
        expected_width = 1280

        assert cropped_img_pil.height == expected_height
        assert cropped_img_pil.width == expected_width
