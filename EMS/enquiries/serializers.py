from rest_framework import serializers
from users.models import User

from enquiries.models import Enquiry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','full_name']


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ['id','message']
