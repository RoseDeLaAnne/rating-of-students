import json as JSON

from django.db.models import Q

from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import *



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        try:
            try:
                if user.student:
                    token['type'] = 'student'
            except:
                if user.professor:
                    token['type'] = 'professor'
        except:
            token['type'] = 'none'
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser


        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class PostPagination(PageNumberPagination):
    page_size = 7

class ApplicationsViewSet(viewsets.ModelViewSet):
    pagination_class = PostPagination
    serializer_class = ApplicationSerializer
    
    def get_queryset(self):
        return Application.objects.all()

class ApplicationsViewSetProfessor(viewsets.ModelViewSet):
    pagination_class = PostPagination
    serializer_class = ApplicationSerializer
    
    def get_queryset(self, *args):
        professor = Professor.objects.get(user__id=self.kwargs['id'])
        return Application.objects.filter(recipient__speciality__department__head=professor).distinct()
        # return Application.objects.filter(sender=sender)

class ApplicationsViewSetStudent(viewsets.ModelViewSet):
    pagination_class = PostPagination
    serializer_class = ApplicationSerializer
    
    def get_queryset(self, *args):
        recipient = Student.objects.get(user__id=self.kwargs['id'])
        return Application.objects.filter(recipient=recipient)

class EventsViewSet(viewsets.ModelViewSet):
    pagination_class = PostPagination
    serializer_class = EventSerializer
    
    def get_queryset(self):
        return Event.objects.all()

class StudentsViewSet(viewsets.ModelViewSet):
    pagination_class = PostPagination
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        return Student.objects.exclude(student_code__isnull=True).exclude(course__isnull=True).exclude(speciality__isnull=True)

@api_view(['GET'])
def CheckStudent(request, username):
    try:
        Student.objects.get(user=User.objects.get(username=username))
        

        return Response(status=200)
    except:
        return Response(status=404)

@api_view(['GET'])
def CheckProfessor(request, username):
    try:
        Professor.objects.get(user=User.objects.get(username=username))
        

        return Response(status=200)
    except:
        return Response(status=404)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetStudent(request, username):
    try:
        student = Student.objects.get(user=User.objects.get(username=username))

        serializer = StudentSerializer(student, many=False)
        

        return Response(serializer.data)
    except:
        return Response(status=404)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetProfessor(request, username):
    try:
        professor = Professor.objects.get(user=User.objects.get(username=username))

        serializer = ProfessorSerializer(professor, many=False)
        

        return Response(serializer.data)
    except:
        return Response(status=404)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetNone(request, username):
    try:
        user = User.objects.get(username=username)

        serializer = UserSerializer(user, many=False)
        

        return Response(serializer.data)
    except:
        return Response(status=404)

# @api_view(['GET'])
# def GetStudents(request):
#     try:
#         students = Student.objects.exclude(student_code__isnull=True).exclude(course__isnull=True).exclude(speciality__isnull=True)

#         serializer = StudentSerializer(students, many=True)
        

#         return Response(serializer.data)
#     except:
#         return Response(status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def GetStudentsByKey(request):
    key = str(request.data['key']).lower()

    students = Student.objects.filter(Q(user__username=key) | Q(user__last_name=key.capitalize()) | Q(user__first_name=key.capitalize()) | Q(user__middle_name=key.capitalize()) | Q(speciality__speciality=key.capitalize()) | Q(speciality__department__name=key.capitalize())).distinct()
    serializer = StudentSerializer(students, many=True)

    return Response(serializer.data, status=200)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def GetApplications(request):
#     try:
#         applications = Application.objects.all()

#         serializer = ApplicationSerializer(applications, many=True)
        

#         return Response(serializer.data)
#     except:
#         return Response(status=500)

class GetApplications(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetEvents(request):
    # try:
    events = Event.objects.all()
    # for i in events:
    #     i.save()

    serializer = EventSerializer(events, many=True)
    

    return Response(serializer.data)
    # except:
    #     return Response(status=500)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetApplication(request, id):
    try:
        application = Application.objects.get(id=id)

        serializer = ApplicationSerializer(application, many=False)
        

        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetEvent(request, id):
    try:
        event = Event.objects.get(id=id)

        serializer = EventSerializer(event, many=False)
        

        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['GET'])
def GetAchievements(request, username):
    try:
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
        achievements = student.application_set.filter(status=1)

        serializer = ApplicationSerializer(achievements, many=True)


        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['POST'])
def CreateStudent(request):
    last_name = request.data['name'].split()[0].capitalize()
    first_name = request.data['name'].split()[1].capitalize()
    middle_name = request.data['name'].split()[2].capitalize()
    username = request.data['username']
    password = request.data['password']


    user = User.objects.create_user(last_name=last_name, first_name=first_name, middle_name=middle_name, username=username, password=password)

    Student.objects.create(user=user)


    return Response(status=200)
    # except:
        # return Response(status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateApplication(request):
    # try:
    event_id = request.data['event_id']
    role_id = request.data['role_id']

    try:
        sender = request.user
        recipient = Student.objects.get(user=request.user)
        status = 0
    except:
        sender_id = request.data['sender_id']
        recipient_id = request.data['recipient_id']
        status = request.data['status']

        sender = User.objects.get(id=sender_id)
        recipient = Student.objects.get(id=recipient_id)
        
    event = Event.objects.get(id=event_id)
    role = Role.objects.get(id=role_id)


    Application.objects.create(event=event, sender=sender, recipient=recipient, role=role, status=status)


    return Response(status=200)
    # except:
        # return Response(status=500)

@api_view(['POST'])
def EditApplication(request):
    try:
        json = JSON.loads(request.data['json'])

        application_id = json['application_id']
        event_id = json['event_id']
        sender_id = json['sender_id']
        recipient_id = json['recipient_id']
        role_id = json['role_id']
        status = json['status']

        event = Event.objects.filter(id=event_id)
        sender = User.objects.filter(id=sender_id)
        recipient = User.objects.get(id=recipient_id)
        role = Role.objects.get(id=role_id)


        application = Application.objects.get(id=application_id)
        application.event = event
        application.sender = sender
        application.recipient = recipient
        application.role = role
        application.status = status

        application.save()


        return Response(status=200)
    except:
        return Response(status=500)

@api_view(['POST'])
def DeleteApplication(request):
    try:
        json = JSON.loads(request.data['json'])

        application_id = json['application_id']

        Application.objects.get(id=application_id).delete()


        return Response(status=200)
    except:
        return Response(status=500)

@api_view(['POST'])
def CreateEvent(request):
    # try:
    if request.FILES:
        json = JSON.loads(request.data['json'])

        image = request.data['files']
        creator_id = json['creator_id']
        name = json['name']
        category_id = json['category_id']
        # status = json['status']
        date_start = json['date_start']
        date_end = json['date_end']

        creator = Professor.objects.get(id=creator_id)
        category = Category.objects.get(id=category_id)


        Event.objects.create(image=image, creator=creator, name=name, category=category, date_start=date_start, date_end=date_end)
    else:
        creator_id = request.data['creator_id']
        name = request.data['name']
        category_id = request.data['category_id']
        # status = request.data['status']
        date_start = request.data['date_start']
        date_end = request.data['date_end']

        creator = Professor.objects.get(id=creator_id)
        category = Category.objects.get(id=category_id)


        Event.objects.create(creator=creator, name=name, category=category, date_start=date_start, date_end=date_end)


    return Response(status=200)
    # except:
    #     return Response(status=500)

@api_view(['POST'])
def EditEvent(request):
    # try:
    if (request.FILES):
        json = JSON.loads(request.data['json'])

        image = request.data['files']
        event_id = json['event_id']
        creator_id = json['creator_id']
        name = json['name']
        category_id = json['category_id']
        status = json['status']
        date_start = json['date_start']
        date_end = json['date_end']

        creator = Professor.objects.get(id=creator_id)
        category = Category.objects.get(id=category_id)


        event = Event.objects.get(id=event_id)
        event.image = image
        event.creator = creator
        event.name = name
        event.category = category
        event.status = status
        event.date_start = date_start
        event.date_end = date_end

        event.save()
    else:
        event_id = request.data['event_id']
        creator_id = request.data['creator_id']
        name = request.data['name']
        category_id = request.data['category_id']
        status = request.data['status']
        date_start = request.data['date_start']
        date_end = request.data['date_end']

        creator = Professor.objects.get(id=creator_id)
        category = Category.objects.get(id=category_id)
        

        event = Event.objects.get(id=event_id)
        event.creator = creator
        event.name = name
        event.category = category
        event.status = status
        event.date_start = date_start
        event.date_end = date_end

        event.save()


    return Response(status=200)
    # except:
        # return Response(status=500)

@api_view(['POST'])
def DeleteEvent(request):
    try:
        json = JSON.loads(request.data['json'])

        event_id = json['event_id']

        Event.objects.get(id=event_id).delete()


        return Response(status=200)
    except:
        return Response(status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSenders(request):
    try:
        senders = User.objects.all()
        # senders = User.objects.filter()

        serializer = UserSerializer(senders, many=True)
        

        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRecipients(request):
    # try:
    recipients = Student.objects.all()
    # recipients = Student.objects.get(user=request.user)

    serializer = StudentSerializer(recipients, many=True)
    

    return Response(serializer.data)
    # except:
        # return Response(status=500)

@api_view(['GET'])
def GetRoles(request):
    try:
        roles = Role.objects.all()

        serializer = RoleSerializer(roles, many=True)
        

        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['GET'])
def GetProfessors(request):
    try:
        professors = Professor.objects.all()

        serializer = ProfessorSerializer(professors, many=True)
        

        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['GET'])
def GetCategories(request):
    try:
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)
        

        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Action(request):
    try:
        page = request.data['page']
        type = request.data['type']
        user_type = request.data['userType']


        match page:
            case 'applications':
                match user_type:
                    case 'student':
                        applications = Application.objects.filter(recipient=Student.objects.get(user=request.user))
                    case 'professor':
                        applications = Application.objects.all()
                    case 'none':
                        applications = Application.objects.all()
                    case _:
                        pass

                serializer = ApplicationSerializer(applications, many=True)


                for id in request.data['ids']:
                    application = Application.objects.get(id=id)                    
                    match type:
                        case 'accept':
                            application.status = 1
                            application.save()
                        case 'waiting':
                            application.status = 0
                            application.save()
                        case 'decline':
                            application.status = -1
                            application.save()
                        case 'delete':
                            if application.status == -1 or application.status == 0 or user_type == 'none':
                                application.delete()
            case 'events':
                events = Event.objects.all()

                serializer = EventSerializer(events, many=True)


                for id in request.data['ids']:
                    event = Event.objects.get(id=id)
                    match type:
                        case 'accept':
                            event.status = 1
                            event.save()
                        case 'decline':
                            event.status = -1
                            event.save()
                        case 'delete':
                            event.delete()
            case _:
                pass


        return Response(serializer.data, status=200)
    except:
        return Response(status=500)

@api_view(['GET'])
def GetActiveEvents(request):
    try:
        events = Event.objects.all()

        serializer = EventSerializer(events, many=True)
        

        return Response(serializer.data)
    except:
        return Response(status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUser(request):
    # try:
    user = request.user
    userType = ''

    if len(Student.objects.filter(user=user)) == 1:
        student = Student.objects.get(user=user)
        userType = 'student'

        serializer = StudentSerializer(student, many=False)
    elif len(Professor.objects.filter(user=user)) == 1:
        professor = Professor.objects.get(user=user)
        userType = 'professor'

        serializer = ProfessorSerializer(professor, many=False)
    else:
        pass
    
    data = {
        'data': serializer.data,
        'userType': userType,
    }


    return Response(data, status=200)
    # except:
    #     return Response(status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserByUsername(request, username):
    try:
        user = User.objects.get(username=username)
        userType = ''

        if len(Student.objects.filter(user=user)) == 1:
            student = Student.objects.get(user=user)
            userType = 'student'

            serializer = StudentSerializer(student, many=False)
        elif len(Professor.objects.filter(user=user)) == 1:
            professor = Professor.objects.get(user=user)
            userType = 'professor'

            serializer = ProfessorSerializer(professor, many=False)
        else:
            pass
        
        data = {
            'data': serializer.data,
            'userType': userType,
        }


        return Response(data, status=200)
    except:
        return Response(status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDepartmentByUsername(request, username):
    professor = Professor.objects.get(user=User.objects.get(username=username))
    department = professor.department_set.all()[0]

    serializer = DepartmentSerializer(department, many=False)


    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetApplicationsByUsername(request, username):
    student = Student.objects.get(user=User.objects.get(username=username))
    applications = student.application_set.all()

    serializer = ApplicationSerializer(applications, many=True)


    return Response(serializer.data, status=200)

# class GetApplicationsByUsername(viewsets.ModelViewSet):
#     def list(self, request, username):
#         student = Student.objects.get(user=User.objects.get(username=username))
#         applications = student.application_set.all()
#         serializer = ApplicationSerializer(applications, many=True)

#         return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Test(request):
    user = request.user

    return Response(status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ApplicationEdit(request, id):
    event_id = request.data['event_id']
    role_id = request.data['role_id']
    status = request.data['status']

    event = Event.objects.get(id=event_id)
    role = Role.objects.get(id=role_id)

    application = Application.objects.get(id=id)
    application.event = event
    application.role = role
    application.status = status

    application.save()


    return Response(status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApplicationsOfDepartments(request):
    applications = []

    department = Department.objects.get(head=Professor.objects.get(user=request.user))
    students = Student.objects.filter(speciality__department=department)
    
    # for i in students:
        # applications.append(Application.objects.filter(recipient=i))
        # print(i)
    
    applications = Application.objects.filter(recipient__speciality__department__head=Professor.objects.get(user=request.user)).distinct()
    print(applications.count())
    for app in applications:
        print(app)
    # serializer = ApplicationSerializer(applications, many=True)

    # return Response(serializer.data, status=200)
    return Response(status=200)

@api_view(['GET'])
def CheckUser(request, username):
    user = User.objects.get(username=username)
    serializer = UserSerializer(user, many=False)

    return Response(status=200)

@api_view(['GET'])
def GetSpecialities(request):
    specialities = Speciality.objects.all()
    serializer = SpecialitySerializer(specialities, many=True)

    return Response(serializer.data, status=200)

@api_view(['POST'])
def SaveAvatar(request):
    json = JSON.loads(request.data['json'])

    username = json['username']
    image = request.data['files']

    user = User.objects.get(username=username)
    user.avatar = image
    user.save()

    return Response(status=200)

@api_view(['POST'])
def SaveStudentData(request):
    username = request.data['username']
    student_code = request.data['student_code']
    speciality_id = request.data['speciality_id']
    course = request.data['course']

    speciality = Speciality.objects.get(id=speciality_id)

    student = Student.objects.get(user__username=username)
    student.student_code = student_code
    student.speciality = speciality
    student.course = course
    student.save()

    return Response(status=200)

@api_view(['POST'])
def SaveUserData(request):
    username = request.data['username']
    usernameC = request.data['usernameC']
    last_name = request.data['last_name']
    first_name = request.data['first_name']
    middle_name = request.data['middle_name']
    email = request.data['email']
    phone_number = request.data['phone_number']
    # password = request.data['password']

    user = User.objects.get(username=username)
    user.username = usernameC
    user.last_name = last_name
    user.first_name = first_name
    user.middle_name = middle_name
    user.email = email
    user.phone_number = phone_number
    # user.password = password
    user.save()

    return Response(status=200)