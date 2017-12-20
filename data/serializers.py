from rest_framework import serializers
from data.models import Blog, User, ApKpi


class BlogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = Blog
        fields = ('title', 'body', 'owner')


# 用于注册的时候返回json数据
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name')


class ApKpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApKpi
        fields = ('title', 'owner')   
