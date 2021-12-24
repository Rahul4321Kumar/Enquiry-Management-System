from django.urls import path
from enquiries.views import EnquiryList, EnquiryDetail

urlpatterns = [  
    path('', EnquiryList.as_view()),                
    path('<int:pk>', EnquiryDetail.as_view()),
]