# from django.shortcuts import render
# from django.contrib.auth import update_session_auth_hash
# from django.contrib import messages
# Create your views here.
# views.py
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from account.serializers import StudentSerializer, TeacherSerializer
from .serializers import LoginSerializer, ProposalTeamSerializer, StudentUserSerializer, TeacherUserSerializer, UserSerializer
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

    # @action(detail=False, methods=['POST'], name='create_teacher_user', url_path=r'teacher/create', serializer_class=TeacherUserSerializer)
    # def create_teacher_user(self, request, *args, **kwargs):
    #     serializer = StudentUserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         teacher = serializer.create(serializer.validated_data)
    #         teacher_serilizer = TeacherSerializer(teacher)
    #         return Response(teacher_serilizer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
