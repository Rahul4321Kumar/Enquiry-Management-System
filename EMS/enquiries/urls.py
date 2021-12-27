from django.urls import include, path
from rest_framework.routers import DefaultRouter

from enquiries.views import EnquiryViewSet


router = DefaultRouter()
router.register('/question/', EnquiryViewSet, basename='question')
urlpatterns = [  
    path('', include(router.urls)),               
]
