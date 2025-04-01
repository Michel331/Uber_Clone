from .models import User
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name','user_type','phone','password','profile_picture')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data.get('email'),
            password = validated_data.get('password'),
            user_type = validated_data.get('user_type'),
            phone = validated_data.get('phone'),
            profile_picture = validated_data.get('profile_picture'),
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','user_type','phone','profile_picture')

