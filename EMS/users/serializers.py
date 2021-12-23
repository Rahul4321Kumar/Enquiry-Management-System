from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "female"),
    )
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
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                "The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            'full_name': self.validated_data.get('full_name', ''),
            'gender': self.validated_data.get('gender', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        print(self.cleaned_data)
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.full_name = self.cleaned_data.get('full_name')
        user.gender = self.cleaned_data.get('gender')
        user.save()
        return user
        