from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from account.filters import BaseFilter
from account.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    # filter_backends = [UserFilter]

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset
    
    @action(detail=False, methods=['GET'], name='logout', url_path=r'logout')
    def logout(self, request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION'):
            _, key = request.META.get('HTTP_AUTHORIZATION').split(' ')
            token = Token.objects.filter(key=key).first()
            if token: token.delete()
        
        return Response({}, status=status.HTTP_200_OK)