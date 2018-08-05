from decouple import config, Csv


TARGET_KEYWORDS = config('TARGET_KEYWORDS', cast=Csv())


def visual_api():
    return True


def find_keywords(json_response):
    keys = json_response.get('labelAnnotations', [])
    return any([key['description'] in TARGET_KEYWORDS for key in keys])
