from django.urls import path, re_path
from .views import *


urlpatterns = [
    path("course_list_api/", Course_ListAPIView.as_view() ),
    path("course_list_api/<int:category_id>/", Course_List_Category.as_view() ),
    path("course_detail_api/<uuid:pk>/", Course_detailAPi.as_view() ),
    path("course_detail_futher_api/<uuid:pk>/", Course_detailApi_futher.as_view() ),
    path("lesson_api/<int:id>/", Lesson_detail_api.as_view() ),
    path('enroll_course/<uuid:pk>/', CourseEnrollmentAPIView.as_view(), name='course_enrollment_api'),
    path("initiate_payment/<uuid:pk>/", PaymentApi.as_view()),
    path("instructor_payment/<uuid:pk>/", Instructor_paymentApi.as_view()),

    path("change_status/", Change_statusAPI.as_view(), name="change_status_api"),
    path("send_email_api/", SendEmailAPIView.as_view(), name="send_email_api"),
    path('search_api/', Search_API.as_view(), name="search_api" ),
    # path('tutor_api/', TutorView.as_view(), name='tutor'),
    # path('create_course_api/', CreateCourseView.as_view(), name='create-course'),



    


    
    


    
]