from django.conf import settings


def get(key, default):
  getattr(settings, key, default)


HASHIDS_MIN_LENGTH = get('HASHIDS_MIN_LENGTH', 8)
