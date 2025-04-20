from storages.backends.s3 import S3Storage


class StaticStorage(S3Storage):
    location = "static"
