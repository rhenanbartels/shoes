import base64
import requests

from decouple import config, Csv


TARGET_KEYWORDS = config('TARGET_KEYWORDS', cast=Csv())
API_VERSION = config('VISION_API_VERSION')
TOKEN = config('VISION_TOKEN')


def vision_api(image_url):
    response = requests.get(image_url)
    base64_image = _prepare_image(response)
    return find_keywords(get_identified_labels(base64_image))


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


def _prepare_image(response):
    return base64.b64encode(response.content).decode()
