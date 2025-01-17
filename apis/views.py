from django.shortcuts import render
from class_app.models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings



class Course_ListAPIView(APIView):

    def get(request, self):
        courses = Course.objects.select_related("category").all()
        category = Category.objects.all()

        course_serializer = CourseListSerializer(courses, many=True)
        category_serializers = CategorySerializer(category, many=True)

        return Response(
            {"course": course_serializer.data, "category": category_serializers.data},
            status=status.HTTP_200_OK,
        )


class Course_List_Category(APIView):

    def get(request, self, category_id):
        category = get_object_or_404(Category, id=category_id)
        courses = Course.objects.select_related("category").filter(category=category)
        categories = Category.objects.all()

        course_serializer = CourseListSerializer(courses, many=True)
        categories_serializer = CategorySerializer(categories, many=True)

        return Response(
            {"course": course_serializer.data, "category": categories_serializer.data},
            status=status.HTTP_200_OK,
        )


class Course_detailAPi(APIView):
    def get(request, self, pk, *args, **kwargs):
        course = Course.objects.get(uu_id=pk)

        course_serializer = CourseDetailSerializer(course)
        return Response(
            {
                "course": course_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class Course_detailApi_futher(APIView):
    def get(self, request, pk):
        course = get_object_or_404(Course, uu_id=pk)
        instructor = course.instructor

        user_profile = get_object_or_404(UserProfile, user=instructor)
        key = user_profile.paystack_key

        enrollment, created = CourseEnrollment.objects.get_or_create(
            user=request.user, course=course
        )
        lessons = Lesson.objects.filter(course=course)
        free_lesson = lessons.filter(is_free=True)
        paid_lessons = lessons.filter(is_free=False)

        course_serializer = CourseDetailSerializer(course)
        # user_profile_serializer = UserProfileSerializer(user_profile)
        paid_lessons_serializers = LessonSerializer(paid_lessons, many=True)
        free_lesson_serializers = LessonSerializer(free_lesson, many=True)

        if enrollment.is_enrolled:

            return Response(
                {"message": "You are already enrolled"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {
                    "course": course_serializer.data,
                    "key": key,
                    "paid_lessons": paid_lessons_serializers.data,
                    "free_lesson": free_lesson_serializers.data,
                },
                status=status.HTTP_200_OK,
            )


class Lesson_detail_api(APIView):

    def get(self, request, id):

        lesson = get_object_or_404(Lesson, id=id)

        lesson_Serializer = LessonSerializer(lesson)

        return Response({"lesson": lesson_Serializer.data}, status=status.HTTP_200_OK)


class CourseEnrollmentAPIView(APIView):

    def post(self, request, pk):
        # Retrieve the course by its UUID
        course = get_object_or_404(Course, uu_id=pk)

        # Get or create a CourseEnrollment for the user
        enrollment, created = CourseEnrollment.objects.get_or_create(
            user=request.user, course=course
        )

        # Mark the enrollment as active
        enrollment.is_enrolled = True
        enrollment.save()

        # Update the course's enrollment status if necessary
        if created:
            course.is_enrolled = True
            course.save()

        # Prepare the serialized response
        course_serializer = CourseDetailSerializer(course)

        return Response(
            {
                "message": (
                    "Enrollment successful." if created else "You are already enrolled."
                ),
                "course": course_serializer.data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


from django.urls import reverse
import requests


class PaymentApi(APIView):

    def post(self, request, pk):
        course = Course.objects.get(uu_id=pk)

        instructor_key = course.instructor

        user_profile = get_object_or_404(UserProfile, user=instructor_key)
        key = user_profile.paystack_key

        paystack_url = "https://api.paystack.co/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

        callback_url = request.build_absolute_uri(
            reverse("course_enrollment_api", args=[pk])
        )

        data = {
            "amount": int(course.price * 100),
            "email": request.user.email,
            "callback_url": callback_url,
        }

        response = requests.post(paystack_url, headers=headers, json=data)
        response_data = response.json()

        if response_data["status"]:
            authorization_url = response_data["data"]["authorization_url"]
            reference = response_data["data"]["reference"]

            # return redirect(authorization_url)
            return Response(
                {"authorization_url": authorization_url}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "An error occured while initiating payment"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Instructor_paymentApi(APIView):
    def post(self, request ):
        paystack_url = 'https://api.paystack.co/transaction/initialize'

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        
        callback_url = request.build_absolute_uri(reverse('change_status_api'))

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
            
            
            return Response({
                "authorization_url" : authorization_url
            }, status=status.HTTP_201_CREATED)
        else:
            # Handle error
            return Response({
                "message" : "An error occurred while initiating payment."
                
            }, status=status.HTTP_400_BAD_REQUEST)

class Change_statusAPI(APIView):
    
    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user = request.user)
        user_profile.status  = "Instructor"
        user_profile.save()
        return Response({
            "message" : "You are now an instructor"
            
        }, status=status.HTTP_201_CREATED)



from django.core.mail import send_mail
from .serializers import EmailSerializer

class SendEmailAPIView(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        # Deserialize and validate input data
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            subject = serializer.validated_data["subject"]
            message = serializer.validated_data["message"]
            your_email = request.user.email  # Authenticated user's email

            # Attempt to send the email
            try:
                send_mail(
                    subject,
                    message,
                    your_email,
                    ["ojugbelelateef2006@gmail.com"],  # Receiver's email address
                    fail_silently=False,
                )
                return Response({"message": "Email sent successfully."}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"error": "Failed to send email.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Q


class Search_API(APIView):
    def post(self, request):
        query = request.data.get('query', '')  # Default to empty string if query is not provided
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        counted = courses.count()

        # Serialize the filtered courses
        serializer = CourseDetailSerializer(courses, many=True)

        return Response({
            "courses": serializer.data,
            "query": query,
            "count": counted
        }, status=status.HTTP_200_OK)


     
     
def function_name():
    pass


# from .serializers import UserProfileSerializer

# class TutorView(APIView):

#     def get(self, request, *args, **kwargs):
#         # Get the user profile based on the logged-in user
#         user_profile = get_object_or_404(UserProfile, user=request.user)
        
#         # Check if the user is an instructor
#         if user_profile.status == "Instructor":
#             # If status is "Instructor", return a redirect URL
#             return Response({"message": "You are now an instructor.You can now add courses"}, status=status.HTTP_200_OK)
#         else:
#             # Otherwise, return the user profile data as JSON
#             serializer = UserProfileSerializer(user_profile)
#             return Response(serializer.data, status=status.HTTP_200_OK)

