import boto3
from botocore.config import Config
from django.conf import settings

from .celery import app as celery_app

config = Config(
    retries=dict(
        max_attempts=60
    )
)

__all__ = ("celery_app", "s3_client", "dynamodb_table")

session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                aws_secret_access_key=settings.AWS_SECRET_KEY,
                                region_name=settings.AWS_REGION_NAME)

s3 = session.resource('s3')
s3_client = s3.meta.client

dynamodb = session.resource('dynamodb', config=config)
dynamodb_table = dynamodb.Table(settings.AWS_DYNAMODB_NAME)
