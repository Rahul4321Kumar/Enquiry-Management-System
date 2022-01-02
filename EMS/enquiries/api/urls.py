from django.urls import include, path
from rest_framework.routers import DefaultRouter

from enquiries.api.views import EnquiryViewSet, users

router = DefaultRouter()
router.register(r"enquiry", EnquiryViewSet, basename="enquiry")


urlpatterns = [
    path("", include(router.urls)),
    path('dummy/', users, name = 'users'),
]        
