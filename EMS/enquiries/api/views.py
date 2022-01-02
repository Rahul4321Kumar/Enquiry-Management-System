import json
from django.http.response import HttpResponse
import requests

from django.shortcuts import render
from enquiries.api.serializers import EnquirySerializer
from enquiries.models import Enquiry
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class EnquiryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnquirySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Enquiry.objects.filter(user=self.request.user)


def users(request):
    #pull data from third party rest api
    response = requests.get('https://jsonplaceholder.typicode2.com/users')
    #convert reponse data into json
    users = response.json()
    print(users)
    return HttpResponse(json.dumps(users), content_type="application/json")
