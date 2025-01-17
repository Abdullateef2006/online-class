from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import ProfileView


urlpatterns = [
    path("logout/", views.signout, name="logout"),
    path("register/", views.signup, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "delete_enrollment/<int:id>/<int:course_id>",
        views.delete_enrollment,
        name="delete_enrollment",
    ),
    path("about_us/", views.about_us, name="about_us"),
    # path('edit_profile/', views.edit_profile, name='edit_profile'),
    path("", views.home, name="home"),
    path("Instructor_profile/<int:id>/", views.Instrctor_profile, name="Instrctor_profile"),
    path("all_profile/", views.all_profile, name="all_profile"),

    path("profile/", views.user_profile, name="user_profile"),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("courses/", views.course_list, name="course_list"),
    path(
        "courses/category/<int:category_id>/",
        views.course_list_by_category,
        name="course_list_category",
    ),
    path(
        "enrolled_courses/<int:course_id>/", views.course_detail, name="course_detail"
    ),
    path("course/<str:pk>/", views.course_details, name="course_details"),
    path(
        "course/<str:pk>/further/",
        views.course_details_further,
        name="course_details_further",
    ),
    path("enrolled-courses/", views.enrolled_courses, name="enroll_courses"),
    path(
        "courses/<int:course_id>/lessons/<int:lesson_id>/",
        views.lesson_detail,
        name="lesson_detail",
    ),
    path(
        "courses/<int:course_id>/assignments/<int:assignment_id>/",
        views.assignment_detail,
        name="assignment_detail",
    ),
    path(
        "courses/<int:course_id>/assignments/<int:assignment_id>/submit/",
        views.submit_assignment,
        name="submit_assignment",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "courses/<int:course_id>/notifications/",
        views.course_notifications,
        name="course_notifications",
    ),
    path("user_chat/<int:user_id>/", views.user_chat, name="user_chat"),
    path("send_message/", views.send_message, name="send_message"),
    path("chat/", views.chats_view, name="chat_view"),
    path("send-email/", views.send_email, name="send_email"),
    path("profile_succesfully updated", views.ProfileComplete, name="Profie_complete"),
    path("initiate_payment/<str:pk>/", views.initiate_payment, name="initiate_payment"),
    # path('payment_callback/', views.payment_callback, name='payment_callback'),
    # path(
    #     "courses/<int:course_id>/enroll/",
    #     views.course_enrollment,
    #     name="course_enrollment",
    # ),
    path(
        "courses/<str:pk>/enroll/",
        views.course_enrollment,
        name="course_enrollment",
    ),
    path("videos/<int:video_id>/", views.video_detail, name="video_detail"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("edit_profile/<int:pk>/", ProfileView.as_view(), name="edit_profile"),
    path("search/", views.searchFeature, name="Search"),
    path("create_course", views.createCourse, name="create_course"),
    path("create_lesson/<str:pk>/", views.createLesson, name="create_lesson"),
    path("edit_course/<str:pk>/", views.edit_course, name="edit_course"),
    path("delete_course/<str:pk>/", views.delete_course, name="delete_course"),
    path("my_courses/", views.your_courses, name="your_courses"),
    path("delete_lesson/<int:id>", views.delete_lesson, name="delete_lesson"),
    path("create_topic/<int:id>/", views.createTopic, name="create_topic"),
    path("delete_topic/<int:id>/", views.delete_topic, name="delete_topic"),
    path("Instructor_payment/", views.Instructor_payment, name="Instructor_payment"),
    path("change_status/", views.change_status, name="change_status"),
    path("become_a_tutor/", views.tutor, name="tutor"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
