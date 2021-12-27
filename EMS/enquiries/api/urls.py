from django.urls import include, path
from rest_framework.routers import DefaultRouter

from enquiries.api.views import EnquiryViewSet

router = DefaultRouter()
router.register(r"enquiry", EnquiryViewSet, basename="enquiry")


urlpatterns = [
    path("", include(router.urls)),
]        
