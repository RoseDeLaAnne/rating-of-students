from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


from .models import *
import datetime
from django.utils import timezone


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        depth = 1

class ProfessorSerializer(ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

        depth = 1

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

        depth = 3

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

        depth = 3

class SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'

        depth = 2

class EventSerializer(ModelSerializer):
    # status = serializers.SerializerMethodField('statusV')

    # def statusV(self, event):
    #     if event.date_start <= timezone.now() <= event.date_end:
    #         return 1
    #     else:
    #         return -1


    class Meta:
        model = Event
        fields = '__all__'

        depth = 2

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

        depth = 1

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

        depth = 1

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

        depth = 1
