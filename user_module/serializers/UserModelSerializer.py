from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from user_module.models import UserProfile


class UserProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio')


class UserModelSerializer(ModelSerializer):
    user_profile = UserProfileModelSerializer()

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_profile')
        extra_kwargs = {'password': {'write_only': True}}
