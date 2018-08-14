from boto3 import Session
from decouple import config


def login():
    session = Session()
    return session.client(
            's3',
            region_name=config('AWS_REGION_NAME'),
            endpoint_url=config('AWS_ENDPOINT_URL'),
            aws_access_key_id=config('AWS_ACCESS_ID'),
            aws_secret_access_key=config('AWS_SECRET_KEY')
    )


def send_image_aws(client, img, img_name):
    client.upload_fileobj(
            img,
            config('AWS_BUCKET_NAME'),
            img_name,
            ExtraArgs={'ContentType': "image/jpeg", "ACL": "public-read"}
    )
