import re
from unittest import TestCase
from django.test import Client
from unittest.mock import patch
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


from enquiries.enquiry_factory import EnquiryFactory
from users.user_factory import UserFactory
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
            self.assertEqual(response.status_code, status.
            HTTP_200_OK)

# class ThirdPartyTestCase(TestCase):

#     @patch('enquiries.api.views.users')
#     def test_user(self, mock_list_user):
#         mock_list_user.return_value.status_code = 200
#         mock_list_user.return_value.json.return_value = {
#     "id": 1,
#     "name": "Leanne Graham",
#     "username": "Bret",
#     "email": "Sincere@april.biz",
#     "address": {
#       "street": "Kulas Light",
#       "suite": "Apt. 556",
#       "city": "Gwenborough",
#       "zipcode": "92998-3874",
#       "geo": {
#         "lat": "-37.3159",
#         "lng": "81.1496"
#       }
#     },
#     "phone": "1-770-736-8031 x56442",
#     "website": "hildegard.org",
#     "company": {
#       "name": "Romaguera-Crona",
#       "catchPhrase": "Multi-layered client-server neural-net",
#       "bs": "harness real-time e-markets"
#     }
#   }
#         client = Client()
#         response = client.get(reverse('users'))
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#         self.assertEqual(response.json()[0]['name'], 'Leanne Graham')


class EnquiryViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
    
    def api_authentication(self):
        self.token = self.get_tokens_for_user()
        print(self.token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def create_enquiry(self):
        enquiry = EnquiryFactory()
        data = {"message": enquiry.message}
        # response = self.client.post(reverse("enquiry-list"), data)
        return enquiry

    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)


class EnquiryListCreateCase(EnquiryViewSetTestCase):

    def test_enquiry_list_authenticated(self):
        self.api_authentication()
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        message = "First value and second value are not equal !"
        self.assertEqual(len(response.data), 0, message)
        
    def test_enquiry_create_with_no_auth(self):
        enquiry = EnquiryFactory()
        data = {"message": enquiry.message}
        response = self.client.post(reverse("enquiry-list"), data)
        self.assertEqual(response.status_code,status.
        HTTP_401_UNAUTHORIZED)
    
    def test_enquiry_create(self):
        self.api_authentication()
        response = self.create_enquiry()
        # import pdb;pdb.set_trace()
        # # self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        # created_data = Enquiry.objects.get(id = response.id)
        # self.assertEqual(created_data.message,response.data['message'])
        

class TestEnquiryDetailView(EnquiryViewSetTestCase):

    def test_retrieve_enquiry_detail(self):
        self.api_authentication()
        response = self.create_enquiry()
        
        res = self.client.get(
            reverse("enquiry-detail",
            kwargs={'pk': response.id})
            )
        import pdb;pdb.set_trace()
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        # enquiry_data = Enquiry.objects.get(id = enquiry.id)
        # message = "First value and second value are not equal !"
        # self.assertEqual(enquiry_data.message, response.data['message'], message)

    def test_retrieve_update_detail(self):
        self.api_authentication()
        response = self.create_enquiry()
        
        update_response = self.client.patch(
            reverse("enquiry-detail",
            kwargs={'pk': response.id}), {
            "message": "New enquiry detail"
        })
        import pdb;pdb.set_trace()
        self.assertEqual(update_response.status_code,status.HTTP_200_OK)
        update_enquiry = Enquiry.objects.get(id=response.id)
        message = "First value and second value are not equal !"
        self.assertEqual(update_enquiry.message, "New enquiry detail", message)

    def test_retrieve_delete_detail(self):
        self.api_authentication()
        response = self.create_enquiry()
        import pdb;pdb.set_trace()
        prev_db_count = Enquiry.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        message = "First value and second value are not equal !"
        self.assertEqual(prev_db_count, 1, message)
        delete_response = self.client.delete(
            reverse("enquiry-detail", kwargs={'pk': response.id})
        )
        self.assertEqual(delete_response.status_code,status.
        HTTP_204_NO_CONTENT)
        message = "First value and second value are not equal !"
        self.assertEqual(Enquiry.objects.all().count(), 1, message)
