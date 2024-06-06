"""
Custom storage backends for s3.
"""

from storages.backends.s3boto3 import S3Boto3Storage


class StaticS3Storage(S3BotoStorage):
    location = "static"
    default_acl = "public-read"


class MediaS3Storage(S3BotoStorage):
    location = "media"
    default_acl = "public-read"
