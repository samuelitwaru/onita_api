# from django.shortcuts import render
# from django.contrib.auth import update_session_auth_hash
# from django.contrib import messages
# Create your views here.
# views.py
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from account.serializers import StudentSerializer, TeacherSerializer
from account.utils.core import get_user_from_bearer_token
from .serializers import LoginSerializer, PasswordChangeSerializer, ProposalTeamSerializer, StudentUserSerializer, TeacherUserSerializer, UserSerializer
# from rest_framework.permissions import IsAuthenticated
# from .serializers import CustomAuthTokenSerializer
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
# from django_filters.rest_framework import DjangoFilterBackend
# from django.conf import settings
# from account.filters import UserFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from account.filters import BaseFilter



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    # filter_backends = [UserFilter]

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset
    
    @action(detail=False, methods=['POST'], name='login', url_path=r'login', serializer_class=LoginSerializer)
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            user_data = UserSerializer(user).data
            user_data['groups'] = [group.name for group in user.groups.all()]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': user_data})
        else:
            return Response({'error': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'], name='create_student_user', url_path=r'student/create', serializer_class=StudentUserSerializer)
    def create_student_user(self, request, *args, **kwargs):
        serializer = StudentUserSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.create(serializer.validated_data)
            student_serilizer = StudentSerializer(student)
            return Response(student_serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'], name='change_user_password', url_path=r'password/change', serializer_class=PasswordChangeSerializer)
    def change_user_password(self, request, pk, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_from_bearer_token(request)
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Check if the old password is correct
            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Change the password and update session authentication hash
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user authenticated

            return Response({'detail': 'Password successfully changed.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)