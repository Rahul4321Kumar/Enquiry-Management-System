from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from enquiries.models import Enquiry
from enquiries.serializers import EnquirySerializer


class EnquiryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnquirySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Enquiry.objects.filter(user=self.request.user)
