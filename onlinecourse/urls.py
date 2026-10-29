from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Route for course list view
    path('', views.CourseListView.as_view(), name='index'),
    # Route for registration
    path('registration/', views.registration_request, name='registration'),
    # Route for login
    path('login/', views.login_request, name='login'),
    # Route for logout
    path('logout/', views.logout_request, name='logout'),
    # Route for course details
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    # Route for enrolling in a course
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),
    # Route for exam submission
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    # Route for showing exam result
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]

