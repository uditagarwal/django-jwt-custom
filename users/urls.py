from django.conf.urls import url

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveAPIView, UserRefreshToken

urlpatterns = [
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^access-tokens/?$', LoginAPIView.as_view()),
    url(r'^access-tokens/refresh?$', UserRefreshToken.as_view()),
    url(r'^me/?$', UserRetrieveAPIView.as_view()),
]
