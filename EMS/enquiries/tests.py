import json,re
# from django.conf import _DjangoConfLazyObject

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core import mail
from rest_framework_jwt.settings import api_settings
from rest_framework.test import APIClient, APITestCase

from users.models import User


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"email": "test@localhost.app", "full_name": "testcase", "gender": "M",
                "password1": "some_strong_psw","password2": "some_strong_psw"}
        response = self.client.post("/auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        match = re.search(r'\?code=([0-9a-f]+)$', mail.outbox[-1].body, re.MULTILINE)
        if match:
            token = match.group(1)
            response = self.client.post("/auth/registration/account-confirm-email/<str:key>/", {'key': token})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        self.user = User.objects.create_user(email='user1@foo.com', password='pass')
        self.user.is_staff = True
        self.user.save()
        response = self.client.post("/auth/login/", {'email':'user1@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)
        self.token = response.data['access_token']
        self.api_authenticated()
        
    def api_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer Token" + self.token)
