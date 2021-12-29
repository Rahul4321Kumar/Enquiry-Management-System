import re

from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from enquiries.models import Enquiry


class RegistrationTestCase(APITestCase):
    
    def test_registration(self):
        data = {
            "email": "test@localhost.app",
            "full_name": "testcase",
            "gender": "M",
            "password1": "some_strong_psw",
            "password2": "some_strong_psw"
           }
        response = self.client.post("/auth/registration/", data)
        self.assertEqual(response.status_code, status.
        HTTP_201_CREATED)
        match = re.search(r'\?code=([0-9a-f]+)$', mail.outbox[-1].body, re.MULTILINE)
        if match:
            token = match.group(1)
            response = self.client.post(
                "/auth/registration/account-confirm-email/<str:key>/",
                {'key': token}
               )
            import pdb;pdb.set_trace()
            self.assertEqual(response.status_code, status.
            HTTP_200_OK)


class EnquiryViewSetTestCase(APITestCase):

    def create_enquiry(self):
        data = {"message": "Hello its new enquiry"}
        response = self.client.post(reverse("enquiry-list"), data)
        return response

    def api_authentication(self):
        self.client.post(
            "/auth/registration/",{
                "email": "test@localhost.app",
                "full_name": "testcase",
                "gender": "M",
                "password1": "some_strong_psw",
                "password2": "some_strong_psw"
            })
        resp = self.client.post(
            "/auth/login/", {
                'email':'test@localhost.app',
                'password':'some_strong_psw'
            },)
        self.assertTrue('access_token' in resp.data)
        self.token = resp.data['access_token']
        print(self.token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")


class EnquiryListCreateCase(EnquiryViewSetTestCase):

    def test_enquiry_list_authenticated(self):
        self.api_authentication()
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_enquiry_create_with_no_auth(self):
        response = self.create_enquiry()
        self.assertEqual(response.status_code,status.
        HTTP_401_UNAUTHORIZED)
    
    def test_enquiry_create(self):
        self.api_authentication()
        response = self.create_enquiry()
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    
class TestEnquiryDetailView(EnquiryViewSetTestCase):

    def test_retrieve_enquiry_detail(self):
        self.api_authentication()
        response = self.create_enquiry()
        
        res = self.client.get(
            reverse("enquiry-detail",
            kwargs={'pk':response.data['id']})
            )
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        enquiry_data = Enquiry.objects.get(id=response.data['id'])
        self.assertEqual(enquiry_data.message,response.data["message"])

    def test_retrieve_update_detail(self):
        self.api_authentication()
        response = self.create_enquiry()
        
        update_response = self.client.patch(
            reverse("enquiry-detail",
            kwargs={'pk':response.data['id']}), {
            "message": "New enquiry detail"
        })
        self.assertEqual(update_response.status_code,status.HTTP_200_OK)
        update_enquiry = Enquiry.objects.get(id=response.data['id'])
        self.assertEqual(update_enquiry.message, "New enquiry detail")

    def test_retrieve_delete_detail(self):
        self.api_authentication()
        response = self.create_enquiry()
        delete_response = self.client.delete(
            reverse("enquiry-detail", kwargs={'pk':response.data['id']})
        )
        self.assertEqual(delete_response.status_code,status.
        HTTP_204_NO_CONTENT)
