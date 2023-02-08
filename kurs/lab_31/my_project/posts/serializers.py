from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Posts, CustomUser


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['id', 'writer', 'title', 'body', 'likes']


class CustomUserSerializer(serializers.ModelSerializer):
    token = None
    ref_token = None

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        token = TokenObtainPairSerializer.get_token(user)
        user.access_token = str(token.access_token)
        return user

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'access_token']
