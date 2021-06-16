from django.contrib.auth.models import User
from rest_framework import serializers

from contester.models import Notification


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class NotificationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    task_id = serializers.IntegerField()
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.task_id = validated_data.get('task_id', instance.task_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
