from rest_framework import serializers
from users.models import Property_registration

from django.contrib.auth import authenticate
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth import get_user_model

User = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name')


class RegisterUserSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    user_login = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ['phone_number', 'name', 'user_login', 'password', 'password_2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            phone_number=self.validated_data['phone_number'],
            name=self.validated_data['name'],
            user_login=self.validated_data['user_login']
        )
        password = self.validated_data['password']
        password_2 = self.validated_data['password_2']

        if password != password_2:
            raise serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password)
        user.save()
        return user


class Post_property_serializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username_from_author")

    class Meta:
        model = Property_registration
        fields = ['property_name', 'amount_per_month', 'detail', 'location', 'property_type', 'property_image']
        # we need to add promise
        read_only_fields = ['owner']

    def get_username_from_author(self, blog_posted_by):
        username = blog_posted_by.owner.username
        return username
