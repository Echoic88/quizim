import django.conf import settings
from django.storages.backends import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = setting.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    location = setting.MEDIAFILES_LOCATION
