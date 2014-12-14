from hashids import Hashids
from django.conf import settings
from django.test import TestCase
from rest_framework import serializers
from drf_hashids_fields.fields import HashidsPrimaryKeyField, HashidsPrimaryKeyRelatedField


class Message(object):
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content
        

class MessageSerializer(serializers.Serializer):
    
    id = HashidsPrimaryKeyField()
    content = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.id = attrs['id']
            instance.content = attrs['content']
            return instance
        return Message(**attrs)


class HashidsPrimaryKeySerializerTests(TestCase):
    
    def test_serialization(self):
        id = 1001
        content = 'foo'
        
        msg = Message(id, content)
        serializer = MessageSerializer(msg)
        
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=settings.HASHIDS_MIN_LENGTH)
        
        self.assertNotEquals(serializer.data.get('id'), msg.id)
        self.assertEquals(serializer.data.get('id'), hashids.encrypt(msg.id))
    
    