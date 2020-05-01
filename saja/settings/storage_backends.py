from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
