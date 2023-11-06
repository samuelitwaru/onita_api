# serializers.py
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from api.models import Level, School, Student, Teacher
from api.serializers import LevelSerializer


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only (not displayed in responses)
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)   
    level = LevelSerializer(read_only=True)   
    class Meta:
        model = Student
        fields = '__all__'

    
class StudentUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    telephone = serializers.CharField()
    email = serializers.EmailField()
    level = serializers.ChoiceField(choices=[(level.id, level.name) for level in Level.objects.all()])
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise serializers.ValidationError(f"User with the email, '{value}' already exists")
        return value

    def create(self, validated_data):
        user = User(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                username=validated_data['email'],
            )
        user.set_password(validated_data['password'])
        user.save()
        student = Student(
            user=user, 
            telephone=validated_data["telephone"],
            full_name=f'{validated_data["first_name"]} {validated_data["last_name"]}',
            level_id=validated_data['level'],
        )
        student.save()
        return student

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TeacherUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    telephone = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                username=validated_data['email'],
            )
        user.set_password(validated_data['password'])
        user.save()
        student = Teacher(
            user=user, 
            telephone=validated_data["telephone"],
            full_name=f'{validated_data["first_name"]} {validated_data["last_name"]}',
        )
        student.save()
        return student


class ProposalTeamSerializer(serializers.Serializer):
    email = serializers.EmailField()

    

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class SetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required= True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        errors = {}
        if not User.objects.filter(username=data.get('email')).first():
            errors['email'] = ["This email does not exist."]
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
# class CompleteSignupSerializer(serializers.Serializer):
#     token = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     phone = serializers.IntegerField()
#     gender = serializers.CharField()
#     faculty = serializers.IntegerField()
#     department = serializers.IntegerField()
#     qualification = serializers.IntegerField()
#     password = serializers.CharField(required=True)
#     confirm_password = serializers.CharField(required=True)
  

#     def validate(self, data):
#         password = data.get('password')
#         confirm_password = data.get('confirm_password')
#         if password != confirm_password:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data
    
    
class UpdateUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.IntegerField()
    faculty = serializers.IntegerField()
    department = serializers.IntegerField()
    qualification = serializers.IntegerField()
    