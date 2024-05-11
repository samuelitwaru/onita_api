from rest_framework import viewsets
from ..serializers import StudentSerializer
from api.models import Student
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from account.filters import BaseFilter
from api.models import Subtopic, Topic
from api.serializers import SubtopicSerializer, UpdateStudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset

    @action(detail=True, methods=['PUT'], name='update_student', url_path=r'update', serializer_class=UpdateStudentSerializer)
    def update_student(self, request, pk, *args, **kwargs):
        student = Student.objects.get(id=pk)
        serializer = UpdateStudentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = student.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.username = data['email']
            student.full_name = f'{data["first_name"]} {data["last_name"]}'
            student.telephone = data["telephone"]
            user.save()
            student.save()
            student = StudentSerializer(student).data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'student':student}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        