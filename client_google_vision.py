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
    base64_image = _prepare_image(response)
    is_target = find_keywords(get_identified_labels(base64_image))
    if is_target:
        return is_target

    return find_keywords(get_identified_labels(crop_image(response.content)))


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
                'maxResults': 5,
            }]

        }]
    }
    header = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=header, json=body)
    return response.json()['responses'][0]


def find_keywords(json_response):
    keys = json_response.get('labelAnnotations', [])
    return any([key['description'] in TARGET_KEYWORDS for key in keys])


def crop_image(img, prop=0.5):
    img_pillow = Image.open(BytesIO(img))
    h = img_pillow.height
    w = img_pillow.width
    cropped_img = img_pillow.crop((0, h * prop, w, h))
    img_buffer = BytesIO()
    cropped_img.save(img_buffer, format='PNG')
    return base64.b64encode(img_buffer.getvalue()).decode()


def _prepare_image(response):
    return base64.b64encode(response.content).decode()
