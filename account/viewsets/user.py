from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from account.filters import BaseFilter
from account.serializers import LoginSerializer, SchoolSerializer, StudentSerializer, StudentUserSerializer, TeacherSerializer, TeacherUserSerializer, UserSerializer
from api.models import School, Student, Teacher
from api.serializers import StudentAnswerSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    # filter_backends = [UserFilter]

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset
    
    @action(detail=False, methods=['POST','GET'], name='login', url_path=r'login', serializer_class=LoginSerializer)
    def login(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
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
    
    @action(detail=False, methods=['POST','GET'], name='create_student_user', url_path=r'student/create', serializer_class=StudentUserSerializer)
    def create_student_user(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
        serializer = StudentAnswerSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.create(serializer.validated_data)
            student_serilizer = StudentSerializer(student)
            return Response(student_serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST','GET'], name='create_teacher_user', url_path=r'teacher/create', serializer_class=TeacherUserSerializer)
    def create_teacher_user(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
        serializer = TeacherUserSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.create(serializer.validated_data)
            teacher_serilizer = TeacherSerializer(teacher)
            return Response(teacher_serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)