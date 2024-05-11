from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from account.filters import BaseFilter
from account.serializers import LoginSerializer, PasswordChangeSerializer, PasswordResetSerializer, SchoolUserSerializer, SetPasswordSerializer, StudentUserSerializer, TeacherUserSerializer, UserSerializer
from account.utils.core import get_user_from_bearer_token
from account.utils.mails import send_html_email
from api.models import School, Student, Teacher
from api.serializers import SchoolSerializer, StudentAnswerSerializer, StudentSerializer, TeacherSerializer
from django.contrib.auth import update_session_auth_hash



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
        serializer = StudentUserSerializer(data=request.data)
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

    @action(detail=False, methods=['POST','GET'], name='create_school_user', url_path=r'school/create', serializer_class=SchoolUserSerializer)
    def create_school_user(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
        serializer = SchoolUserSerializer(data=request.data)
        if serializer.is_valid():
            school = serializer.create(serializer.validated_data)
            school_serilizer = SchoolSerializer(school)
            return Response(school_serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['PUT','GET'], name='change_user_password', url_path=r'change-password', serializer_class=PasswordChangeSerializer)
    def change_user_password(self, request, pk, *args, **kwargs):
        if request.method == 'GET': return Response({})
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_from_bearer_token(request)
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Check if the old password is correct
            if not user:
                return Response({'detail': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
            if user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Change the password and update session authentication hash
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user authenticated

            return Response({'detail': 'Password successfully changed.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST','GET'], name='reset_user_password', url_path=r'reset-password', serializer_class=PasswordResetSerializer)
    def reset_password(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            # set token
            data = serializer.data
            user = User.objects.filter(username=data.get('email')).first()
            token, created = Token.objects.get_or_create(user=user)
            # send email token
            context = {
                'user': user, 'token':token, 'client_address': settings.CLIENT_ADDRESS
                }
            send_html_email(
                request,
                'PASSWORD RESET',
                [user.username],
                'emails/password-reset.html',
                context
                )
            return Response({'detail': 'A link has been sent to your email. Click the link to reset your password'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST','GET'], name='set_user_password', url_path=r'set-password', serializer_class=SetPasswordSerializer)
    def set_password(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # set token
            data = serializer.data
            token = Token.objects.get(key=data['token'])
            if token:
                user = token.user
                user.set_password(data['new_password'])
                user.save()
                return Response({'detail': 'Your password has been updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)