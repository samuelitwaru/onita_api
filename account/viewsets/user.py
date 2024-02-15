from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from account.filters import BaseFilter
from account.serializers import LoginSerializer, SchoolSerializer, StudentSerializer, TeacherSerializer, UserSerializer
from api.models import School, Student, Teacher



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
        if request.method == 'GET':
            return Response({})
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            # user_data = UserSerializer(user).data
            # user_data['groups'] = [group.name for group in user.groups.all()]
            student = StudentSerializer(Student.objects.filter(user=user).first()).data
            teacher = TeacherSerializer(Teacher.objects.filter(user=user).first()).data
            school = SchoolSerializer(School.objects.filter(user=user).first()).data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'student':student, 'teacher':teacher, 'school':school})
        else:
            return Response({'error': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['GET'], name='logout', url_path=r'logout')
    def logout(self, request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION'):
            _, key = request.META.get('HTTP_AUTHORIZATION').split(' ')
            token = Token.objects.filter(key=key).first()
            if token: token.delete()
        
        return Response({}, status=status.HTTP_200_OK)