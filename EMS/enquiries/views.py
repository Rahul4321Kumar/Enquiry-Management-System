from django.shortcuts import render

from enquiries.serializers import EnquirySerializer
from enquiries.models import Enquiry
from rest_framework.generics import ListCreateAPIView,  RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


class EnquiryList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer


class EnquiryDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer
