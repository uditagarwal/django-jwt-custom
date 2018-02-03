from django.conf.urls import url

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveAPIView

urlpatterns = [
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^access-tokens/?$', LoginAPIView.as_view()),
    url(r'^me/?$', UserRetrieveAPIView.as_view()),
]
