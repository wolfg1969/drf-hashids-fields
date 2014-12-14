from django.conf import settings
from rest_framework import serializers
from hashids import Hashids


class HashidsPrimaryKeyField(serializers.Field):

    def __init__(self, *args, **kwargs):
        salt = kwargs.pop('salt', settings.SECRET_KEY)
        min_length = kwargs.pop('min_length', settings.HASHIDS_MIN_LENGTH)
        self.hashids = Hashids(salt=salt, min_length=min_length)
        super(HashidsPrimaryKeyField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        return self.hashids.encrypt(value)


class HashidsPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def __init__(self, *args, **kwargs):
        salt = kwargs.pop('salt', settings.SECRET_KEY)
        min_length = kwargs.pop('min_length', settings.HASHIDS_MIN_LENGTH)
        self.hashids = Hashids(salt=salt, min_length=min_length)
        super(HashidsPrimaryKeyRelatedField, self).__init__(*args, **kwargs)

    def to_native(self, pk):
        return self.hashids.encrypt(pk)

    def from_native(self, data):
        pk = self.hashids.decrypt(data)[0]
        return super(HashidsPrimaryKeyRelatedField, self).from_native(pk)