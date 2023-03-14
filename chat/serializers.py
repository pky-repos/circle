from rest_framework import serializers
from users.models import Profile
from users.serializers import ProfileSerializer
from .models import ChatGroup, Message, Like


class ChatGroupSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(required=False, many=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = ChatGroup
        fields = ['id', 'name', 'profiles']


class ChatGroupAddUserSerializer(serializers.ModelSerializer):
    profiles = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True, many=True,
                                                  required=False)

    class Meta:
        model = ChatGroup
        fields = ['id', 'profiles']

    def update(self, instance, validated_data):
        profiles = validated_data.pop('profiles')
        instance = super().update(instance, validated_data)

        for profile in profiles:
            instance.profiles.add(profile)

        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def to_internal_value(self, data):
        request = self.context['request']
        profile = request.user.profile

        data.update({
            'profile': profile.id,
        })
        return super().to_internal_value(data)


class LikeReadSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = Like
        fields = ['id', 'profile']


class MessageSerializer(serializers.ModelSerializer):
    likes = LikeReadSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        extra_fields = ['likes']

    def to_internal_value(self, data):
        request = self.context['request']
        profile = request.user.profile

        request.data.update({
            'profile': profile.id,
        })

        # inbuilt field type and object exists validations
        return super().to_internal_value(request.data)
