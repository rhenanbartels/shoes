import base64
import requests

from io import BytesIO

from decouple import config, Csv
from PIL import Image


TARGET_KEYWORDS = config('TARGET_KEYWORDS', cast=Csv())
API_VERSION = config('VISION_API_VERSION')
TOKEN = config('VISION_TOKEN')


def vision_api(image_url):
    response = requests.get(image_url)
    img_obj = BytesIO(response.content)
    base64_image = _prepare_image(response)
    for prop in [(0, 1.0), (0.5, 1.0), (0.75, 1.0), (0.5, 0.75)]:
        is_target = find_keywords(
                get_identified_labels(crop_image(base64_image, prop))
        )
        if is_target:
            return is_target, img_obj

    return False, img_obj


def get_identified_labels(base64_image):
    url = 'https://vision.googleapis.com/{api_version}/images:annotate?'\
          'key={token}'.format(api_version=API_VERSION, token=TOKEN)
    body = {
        'requests': [{
            'image': {
                'content': base64_image,
            },
            'features': [{
                'type': 'LABEL_DETECTION',
                'maxResults': 10,
            }]

        }]
    }
    header = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=header, json=body)
    return response.json()['responses'][0]


def find_keywords(json_response):
    keys = json_response.get('labelAnnotations', [])
    return any([key['description'] in TARGET_KEYWORDS for key in keys])


def crop_image(img, prop=(0.5, 1.0)):
    img_pillow = Image.open(BytesIO(base64.b64decode(img)))
    h = img_pillow.height
    w = img_pillow.width
    cropped_img = img_pillow.crop((0, h * prop[0], w, h * prop[1]))
    img_buffer = BytesIO()
    cropped_img.save(img_buffer, format='PNG')
    return base64.b64encode(img_buffer.getvalue()).decode()


def _prepare_image(response):
    return base64.b64encode(response.content).decode()
