from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from django.conf import settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import authenticate
from django.urls import exceptions as url_exceptions

from rest_framework import serializers, exceptions

from users.models import GENDER_CHOICES, User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    full_name = serializers.CharField(max_length=30)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address."
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        import pdb;pdb.set_trace()
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            "full_name": self.validated_data.get("full_name", ""),
            "gender": self.validated_data.get("gender", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.full_name = self.cleaned_data.get("full_name")
        user.gender = self.cleaned_data.get("gender")
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, email, password):
        from allauth.account import app_settings

        # Authentication through email
        if (
            app_settings.AUTHENTICATION_METHOD
            == app_settings.AuthenticationMethod.EMAIL
        ):
            return self._validate_email(email, password)

    def get_auth_user(self, email, password):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.

        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if "allauth" in settings.INSTALLED_APPS:

            try:
                return self.get_auth_user_using_allauth(email, password)
            except url_exceptions.NoReverseMatch:
                msg = "Unable to log in with provided credentials."
                raise exceptions.ValidationError(msg)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = self.get_auth_user(email, password)

        if not user:
            msg = "Unable to log in with provided credentials."
            raise exceptions.ValidationError(msg)

        attrs["user"] = user
        return attrs


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
            'full_name'
        )
        read_only_fields = ('pk', 'email',)