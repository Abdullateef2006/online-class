from .forms import RegisterForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Lesson, Notification, ChatMessage, CourseEnrollment, Assignment, AssignmentSubmission, UserProfile
from .forms import AssignmentSubmissionForm, CourseForm, EmailForm, UserProfileForm, SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Q
from django.core.mail import send_mail
import requests
from django. contrib import messages

lambda x: x


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "registration/register.html", {"form": form})


def signout(request):
    logout(request)

    return render(request, "registration/logout.html")


def enrolled_courses(request):
    if request.user.is_authenticated:
        course_count = CourseEnrollment.objects.all().filter(user=request.user, is_enrolled = True).count()
        enrolled_courses = CourseEnrollment.objects.all().filter(user=request.user, is_enrolled = True)
        return render(request, "enrolled_courses.html", {"enrolled_courses": enrolled_courses,"course_count" : course_count})


# L


def submit_assignment(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    user = request.user
    course =  Course.objects.get(id=assignment_id)
    submission = AssignmentSubmission.objects.filter(
        assignment=assignment, submitted_by=user
    ).first()

    if request.method == "POST":
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            if submission:
                # User has already submitted, so update the existing submission
                submission.text_submission = form.cleaned_data.get(
                    "text_submission")
                submission.file_submission = form.cleaned_data.get(
                    "file_submission")
                submission.save()
            else:
                # Create a new assignment submission instance
                submission = AssignmentSubmission()
                submission.assignment = assignment
                submission.submitted_by = user
                submission.course = assignment.course
                submission.text_submission = form.cleaned_data.get(
                    "text_submission")
                submission.file_submission = form.cleaned_data.get(
                    "file_submission")
                submission.save()

            # Redirect to the assignment_submitted_successful template
            return render(request, "assignment_submitted_successful.html")

    else:
        form = AssignmentSubmissionForm()

    return render(
        request,
        "submit_assignment.html",
        {"form": form, "assignment": assignment, "submission": submission, 'course':course},
    )


# User Dashboard View
def dashboard(request):
    enrolled_courses = CourseEnrollment.objects.filter(user=request.user)
    courses = Course.objects.all()
    course_count = enrolled_courses.count()
    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        "enrolled_courses": enrolled_courses,
        "courses": courses,
        "user_profile": user_profile,
        "course_count" : course_count
    }

    return render(request, "dashboard.html", context)


# Course Notifications View
def course_notifications(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    notifications = Notification.objects.filter(
        course=course).order_by("-created_at")
    return render(
        request,
        "course_notifications.html",
        {"course": course, "notifications": notifications},
    )


def home(request):
    # Logic to display the home page
    return render(request, "home.html")


@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)
    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(
        request, "user_profile.html", {
            "form": form, "user_profile": user_profile}
    )



from django.shortcuts import render, get_object_or_404
from .models import Course, Category

def course_list(request):
    courses = Course.objects.select_related('category').all()
    categories = Category.objects.all()
    return render(request, 'course_list.html', {'courses': courses, 'categories': categories})

def course_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.select_related('category').filter(category=category)
    categories = Category.objects.all()
    return render(request, 'course_list.html', {'courses': courses, 'categories': categories})


def course_detail(request, course_id):
    
    course = get_object_or_404(Course, id=course_id)
    return render(request, "course_detail.html", {"course": course})

def course_details_further(request, pk):
    course = get_object_or_404(Course, uu_id=pk)
    instructor_key = course.instructor
    
    user_profile = get_object_or_404(UserProfile, user = instructor_key)
    key = user_profile.paystack_key
    
    enrollment,  created = CourseEnrollment.objects.get_or_create(user=request.user, course=course)
    # enrollment.is_enrolled = False
    # enrollment.save()
    if enrollment.is_enrolled:
        lessons = Lesson.objects.filter(course=course)
        free_lessons = lessons.filter(is_free=True)
        paid_lessons = lessons.filter(is_free=False)
        return render(request, "course_details_further_enrolled.html", {"course": course, "free_lessons": free_lessons, "paid_lessons": paid_lessons, "key" : key} )

        # return render(request, "course_details_further.html", {"course": course, "free_lessons": free_lessons, "paid_lessons": paid_lessons, "key" : key} )
    else:
        lessons = Lesson.objects.filter(course=course)
        free_lessons = lessons.filter(is_free=True)
        paid_lessons = lessons.filter(is_free=False)
        return render(request, "course_details_further.html", {"course": course, "free_lessons": free_lessons, "paid_lessons": paid_lessons, "key" : key} )

def course_details(request, pk):
    
    course = get_object_or_404(Course, uu_id=pk)
    if course.instructor == request.user:
            
        # Logic to display course details
        lessons = Lesson.objects.filter(course=course)

        # free_lessons = lessons.filter(is_free=True)
        paid_lessons = lessons.all()
        return render(request, "instructor_course_details_unenrolled.html", {"course": course,  "paid_lessons": paid_lessons} )
    else:
         # Logic to display course details
        lessons = Lesson.objects.filter(course=course)

        free_lessons = lessons.filter(is_free=True)
        paid_lessons = lessons.filter(is_free=False)
        return render(request, "course_details_unenrolled.html", {"course": course, "free_lessons": free_lessons, "paid_lessons": paid_lessons} )




def lesson_detail(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Logic to display lesson details
    return render(request, "lesson_detail.html", {"lesson": lesson})


def assignment_detail(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = get_object_or_404(Course, id=course_id)
    # Logic to display assignment details
    return render(
        request, "assignment_detail.html", {
            "course": course, "assignment": assignment}
    )


def video_detail(request, video_id):
    video = get_object_or_404(Course, id=video_id)
    return render(request, "video_detail.html", {"video": video})


def about_us(request):
    return render(request, 'about_us.html')
    
from django.shortcuts import get_object_or_404

@login_required
def course_enrollment(request, pk):
    course = get_object_or_404(Course, uu_id=pk)
    enrollment,  created = CourseEnrollment.objects.get_or_create(user=request.user, course=course)
    enrollment.is_enrolled = True
    enrollment.save()
    if created:
        course.is_enrolled = True
        enrollment.is_enrolled = True
        enrollment.save()
        course.save()
        return render(request, 'enrollment_success.html', {'course': course})
    else:
        return render(request, 'enrollment_success.html', {'course': course})

        # return render(request, 'enrollment_done.html', {'course': course})

        
    
 
 
  

# @login_required
# def course_enrollment(request, course_id):
#     course = Course.objects.get(id=course_id)
#     enrollment,  created = CourseEnrollment.objects.get_or_create(user=request.user, course=course)
#     if created:
#         course.is_enrolled = True
#         enrollment.is_enrolled = True
#         enrollment.save()
#         course.save()
#         return render(request, 'enrollment_success.html', {'course': course})

#     else:
#         return render(request, 'enrollment_done.html', {'course': course})
    
 
 
  
def delete_enrollment(request, id, course_id):
    enrollment = CourseEnrollment(id=id)
    course = Course.objects.get(id=course_id)

    
    if request.method == 'POST':
        enrollment.delete()
        return redirect('enroll_courses')
    context = {
        'enrollment' : enrollment,
        'course': course
    }
    return render(request, 'delete_enrollment.html', context)
    

import paystack
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Course

# def initiate_payment(request, course_id):
#     course = Course.objects.get(pk=course_id)
#     user = request.user

#     paystack_secret_key = 'sk_test_2de22e65cd85be13d98741474297a8e5bf84dcf5'
#     paystack_api = paystack.Api(secret_key=paystack_secret_key)

#     payment_data = {
#         "email": user.email,
#         "amount": int(course.price * 100),
#         "reference": f"course_{course_id}_payment_{user.id}",
#     }

#     payment_response = paystack_api.transaction.initialize(payment_data)

#     return redirect(payment_response['data']['authorization_url'])



from django.urls import reverse

@login_required(login_url='login')
def initiate_payment(request, pk):
    course = Course.objects.get(uu_id=pk)
    
    instructor_key = course.instructor
    
    user_profile = get_object_or_404(UserProfile, user = instructor_key)
    key = user_profile.paystack_key


    paystack_url = 'https://api.paystack.co/transaction/initialize'

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    }
    
    callback_url = request.build_absolute_uri(reverse('course_enrollment', args=[pk]))

    data = {
        'amount': int(course.price * 100), 
        'email': request.user.email,
        'callback_url': callback_url

    }

    response = requests.post(paystack_url, headers=headers, json=data)
    response_data = response.json()

    if response_data['status']:
        authorization_url = response_data['data']['authorization_url']
        reference = response_data['data']['reference']


        return redirect(authorization_url)
    else:
        return HttpResponse('An error occurred while initiating payment.')
    
    
    
def Instructor_payment(request):
    
    paystack_url = 'https://api.paystack.co/transaction/initialize'

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    
    callback_url = request.build_absolute_uri(reverse('change_status'))

    data = {
        'amount': 3000 * 100, 
        'email': request.user.email,
        'callback_url': callback_url

    }

    response = requests.post(paystack_url, headers=headers, json=data)
    response_data = response.json()

    if response_data['status']:
        authorization_url = response_data['data']['authorization_url']
        reference = response_data['data']['reference']
        
        
        return redirect(authorization_url)
    else:
        # Handle error
        return HttpResponse('An error occurred while initiating payment.')

# def payment_callback(request):
#     reference = request.GET.get('reference')

#     verify_transaction = PaystackTransaction.verify(reference)

#     if verify_transaction == 'success':
#         # course_id = int(verify_transaction['data']['metadata']['course_id'])
#         # course = Course.objects.get(pk=course_id)

#         # existing_enrollment = CourseEnrollment.objects.filter(user=request.user, course=course)

#         # if not existing_enrollment.exists():
#         #     enrollment = CourseEnrollment(user=request.user, course=course)
#         #     enrollment.save()
        
#         return render(request, 'payment_success.html')
#     else:
#         return render(request, 'payment_failed.html')




def send_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            Your_email = request.user.email
            send_mail(
                subject,
                message,
                Your_email,
                ["ojugbelelateef2006@gmail.com"],
                fail_silently=False,
            )
            return render(request, "Email_sent.html")

    else:
        form = EmailForm()

    return render(request, "email_form.html", {"form": form})


# views.py


@login_required
@csrf_exempt
def chats_view(request):
    admin_user = User.objects.filter(is_staff=True).first()

    if not admin_user:
        return HttpResponse(
            "Admin user not found."
        )  # Handle the case where no admin user exists

    if request.method == "POST":
        content = request.POST.get("content")

        # Create and save a message
        message = ChatMessage(sender=request.user,
                              receiver=admin_user, content=content)
        message.save()

    messages_sent_to_admin = ChatMessage.objects.filter(receiver=admin_user).order_by(
        "timestamp"
    )
    messages_sent_by_admin = ChatMessage.objects.filter(sender=admin_user).order_by(
        "timestamp"
    )
    available_users = User.objects.exclude(username=admin_user.username)
    return render(
        request,
        "chat.html",
        {
            "admin_user": admin_user,
            "messages_sent_by_admin": messages_sent_by_admin,
            "messages_sent_to_admin": messages_sent_to_admin,
            "available_users": available_users,
        },
    )


@login_required
@csrf_exempt
def user_chat(request, user_id):
    admin_user = User.objects.filter(is_staff=True).first()

    if not admin_user:
        return HttpResponse(
            "Admin user not found."
        )  # Handle the case where no admin user exists

    selected_user = User.objects.get(id=user_id)

    if request.method == "POST":
        content = request.POST.get("content")

        # Create and save a message
        message = ChatMessage(
            sender=selected_user, receiver=admin_user, content=content
        )
        message.save()

        # Return the message content in the response

    # Fetch messages between the admin and the selected user
    messages_between_admin_and_user = ChatMessage.objects.filter(
        (Q(sender=admin_user) & Q(receiver=selected_user))
        | (Q(sender=selected_user) & Q(receiver=admin_user))
    ).order_by("timestamp")

    return render(
        request,
        "user_chat.html",
        {
            "admin_user": admin_user,
            "selected_user": selected_user,
            "messages_between_admin_and_user": messages_between_admin_and_user,
        },
    )


@login_required
def send_message(request):
    if request.method == "POST":
        content = request.POST.get("content")
        selected_user_id = request.POST.get("selected_user")

        # Check if the selected_user_id is not empty and is a valid integer
        if selected_user_id and selected_user_id.isdigit():
            selected_user = User.objects.get(id=selected_user_id)

            # Create and save a message
            message = ChatMessage(
                sender=request.user, receiver=selected_user, content=content
            )
            message.save()
        else:
            pass
    else:
        pass


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = RegisterForm
    template_name = "edit_profile.html"
    queryset = User.objects.all()
    success_url = reverse_lazy("Profie_complete")
    success_message = "Profile Updated Successfully"


def ProfileComplete(request):
    return render(request, "Profie_complete.html")


    
def searchFeature(request):
    if request.method == 'POST':
        query = request.POST['search_term'].title()
        course = Course.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)  )
        counted = course.count()

        context = {
            'courses': course,
            'query': query,
            'count' : counted
        }
        return render(request, 'base.html', context)
    else:
        return render(request, 'base.html')


from django.shortcuts import render

# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)


# custom 404 view
def custom_500(request, exception):
    return render(request, '500.html', status=500)

def change_status(request):
    user_profile = get_object_or_404(UserProfile, user = request.user)
    user_profile.status  = "Instructor"
    user_profile.save()
    return render(request, 'change_status.html', {})


def tutor(request):
    user_profile = get_object_or_404(UserProfile, user = request.user)
    if user_profile.status  == "Instructor":
        return redirect("create_course")
    else:
        return render(request, 'tutor.html', {})
    
        
          
        
def createCourse(request):
    user_profile = get_object_or_404(UserProfile, user = request.user)
    if user_profile.status == "Instructor":
        
        if request.method == "POST":
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)
                course.instructor = request.user
                course.is_enrolled = True
                course.save()
                user_profile.courses.add(course)

                return redirect('your_courses')
        else:
            form = CourseForm()
            
    else:
        return redirect("tutor")
    return render(request, 'course_creation.html', {'form': form})


    
from django.http import HttpResponseForbidden
    
def edit_course(request, pk):
    course = get_object_or_404(Course, uu_id=pk)
    if course.instructor != request.user:
        return HttpResponseForbidden("You are not allowed to edit this course")
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES,  instance=course)
        if form.is_valid():
            form.save()
            return redirect('your_courses')
    else:
        form = CourseForm()
    return render(request, 'edit_course.html', {'form': form})

def delete_course(request, pk):
    course = Course.objects.get(uu_id = pk)
    if course.instructor != request.user:
        return HttpResponseForbidden("You are not allowed to delete this course")
    if request.method == 'POST':
        course.delete()
        return redirect('your_courses')
    return render(request, 'delete_course.html', {'course': course})
    
    
    
def your_courses(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'your_course.html', {'course' : courses})


def all_profile(request):
    profile = UserProfile.objects.filter(status="Instructor")
    return render(request, 'all_profile.html', {'profile':profile})
    
def Instrctor_profile(request,id):
    profile = UserProfile.objects.get(id=id, status='Instructor')
    courses = profile.courses.all()
    return render(request, 'Instrctor_profile.html', {'profile':profile, 'courses':courses})
    

# def your_courses_detail(request, pk):
#     course = Course.objects.get(uu_id = pk)
#     return render(request, 'delete_course.html', {'course': course})

from .forms import *
def createLesson(request, pk):
    course = get_object_or_404(Course, uu_id=pk)

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            course.is_enrolled = True
            lesson.save()
            return redirect('your_courses')
    else:
        form = LessonForm()
    return render(request, 'lesson_creation.html', {'form': form, 'course': course})


def delete_lesson(request, id):
    lesson = Lesson.objects.get(id = id)

    if request.method == 'POST':
        lesson.delete()
        return redirect('your_courses')
    return render(request, 'delete_lesson.html', {'lesson': lesson})

def createTopic(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    if request.method == "POST":
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.lesson = lesson
            topic.save()
            return redirect('your_courses')
    else:
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.lesson = lesson
            topic.save()
            return redirect('your_courses')
    return render(request, 'topic_creation.html', {'form': form, })


def delete_topic(request, id):
    topic = Topic.objects.get(id=id)

    if request.method == 'POST':
        topic.delete()
        return redirect('your_courses')
    return render(request, 'delete_lesson.html', {'topic': topic})
    
    
    
        
    
        
            
        
    
    
    
