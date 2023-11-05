from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.viewsets import UserViewSet
from onita_api import router

# Create a router and register our viewset with it.
router.register(r'users', UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]