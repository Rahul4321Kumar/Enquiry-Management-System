from rest_framework import serializers
from users.models import User

from enquiries.models import Enquiry


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ['id','message']
        read_only_fields = ('active', 'resolved',)