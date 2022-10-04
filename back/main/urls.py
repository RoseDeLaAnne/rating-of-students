from email.mime import base
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from .views import *

from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'applications', GetApplications)
router.register(r'applications', ApplicationsViewSet, basename='applications')
router.register(
    r'applications-professor/(?P<id>\d+)',
    ApplicationsViewSetProfessor,
    basename='applications-professor'
)
router.register(
    r'applications-student/(?P<id>\d+)',
    ApplicationsViewSetStudent,
    basename='applications-student'
)
router.register(r'events', EventsViewSet, basename='events')
router.register(r'students', StudentsViewSet, basename='students')
# router.register(r'applications-by-username', GetApplicationsByUsername, basename='application')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),

    
    # path('user/<str:username>/', GetUser),

    path('check-student/<str:username>/', CheckStudent),
    path('check-professor/<str:username>/', CheckProfessor),
    path('check-user/<str:username>/', CheckUser),

    path('student/<str:username>/', GetStudent),
    path('professor/<str:username>/', GetProfessor),
    path('none/<str:username>/', GetNone),

    # path('students/', GetStudents),
    # path('applications/', GetApplications),
    path('events/', GetEvents),
    path('active-events/', GetActiveEvents),

    path('application/<int:id>/', GetApplication),
    path('event/<int:id>/', GetEvent),

    path('achievements/<str:username>/', GetAchievements),

    path('create-student/', CreateStudent),

    path('create-application/', CreateApplication),
    path('edit-application/', EditApplication),
    path('delete-application/', DeleteApplication),

    path('create-event/', CreateEvent),
    path('edit-event/', EditEvent),
    path('delete-event/', DeleteEvent),
    
    path('senders/', GetSenders),
    path('recipients/', GetRecipients),
    path('roles/', GetRoles),
    path('categories/', GetCategories),

    path('professors/', GetProfessors),


    path('action/', Action),


    path('user/', GetUser),
    path('user/<str:username>/', GetUserByUsername),

    path('department/<str:username>/', GetDepartmentByUsername),
    path('applicationsu/<str:username>/', GetApplicationsByUsername),

    path('test/', Test),

    path('application/edit/<int:id>/', ApplicationEdit),

    # path('applications-of-departments/', ApplicationsOfDepartments),

    path('students-by-key/', GetStudentsByKey),

    path('specialities/', GetSpecialities),

    path('save-avatar/', SaveAvatar),
    path('save-student-data/', SaveStudentData),
    path('save-user-data/', SaveUserData),
]
