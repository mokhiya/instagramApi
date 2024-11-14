from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from django.utils import timezone

from users.models import CustomUser, VerificationModel, FollowModel


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, max_length=55)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return CustomUser.objects.create_user(**validated_data)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Passwords must match')
        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return attrs

    def validate_email(self, email):
        if not email.endswith('@gmail.com') or email.count('@') != 1:
            raise serializers.ValidationError('Email is not correct')
        return email


class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(email=attrs['email'])
            user_code = VerificationModel.objects.get(user=user, code=attrs['code'])
        except VerificationModel.DoesNotExist:
            raise serializers.ValidationError('Gmail or code is not correct')

        current_time = timezone.now()
        if user_code.created_at + timedelta(minutes=2) < current_time:
            user_code.delete()
            raise serializers.ValidationError("Code is expired")
        attrs['user_code'] = user_code
        return attrs


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')
        try:
            if email_or_username.endswith('@gmail.com'):
                user = CustomUser.objects.get(email=email_or_username)
            else:
                user = CustomUser.objects.get(username=email_or_username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Gmail or username or password is not correct')

        authenticated_user = authenticate(username=user.username, password=user.password)
        if not authenticated_user:
            raise serializers.ValidationError('Email or username or password is not correct')

        attrs['user'] = authenticated_user
        return attrs


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Email is not correct')

        user_code = VerificationModel.objects.filter(user__email=email)
        if user_code:
            current_time = timezone.now()
            if user_code.created_at + timedelta(minutes=2) > current_time:
                raise serializers.ValidationError("You already have active code")
        attrs['user_code'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password', 'groups', 'user_permissions', 'is_superuser']
        read_only_fields = ['is_staff', 'is_active', 'date_joined', 'last_login']


class FollowingSerializer(serializers.ModelSerializer):
    to_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = FollowModel
        fields = ['id', 'created_at', 'to_user']

    # def validate(self, attrs):
    #     user = self.context['request'].user
    #     to_user = attrs.get('to_user')
    #     if to_user == user:
    #         raise serializers.ValidationError('You cannot follow yourself')
    #     return attrs
