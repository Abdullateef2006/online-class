# models.py

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from django.db import models

import uuid



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    uu_id = models.UUIDField(default=uuid.uuid4,  unique=True)
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    language = models.CharField(max_length=200, null=True)
    requirements = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')  # No static default
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(
        User, related_name="enrolled_courses", blank=True)
    img = models.ImageField(upload_to="images/", default=None)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  
    
    is_enrolled = models.BooleanField(default=False)# Optional for paid courses
    learn = models.TextField(null=True)
    level = models.CharField(
        max_length=20, choices=[("Begginer", "Begginer"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")], blank=True)
    

    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content_type = models.CharField(
        max_length=20, choices=[("text", "Text"), ("video", "Video"), ("quiz", "Quiz")]
    )
    content = models.CharField(max_length=250)
    description = models.CharField(blank=True, max_length=250)
    is_free = models.BooleanField(
        default=False
    )  
    



class Topic(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_free = models.BooleanField(
        default=False
    )  
    video_file = models.FileField(
        upload_to="topic_videos/", blank=True, null=True)
    pdf_file = models.FileField(upload_to="topic_pdfs/", blank=True, null=True)
    
    def __str__(self) :
        return self.title


class Discussion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)


class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField()


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Assuming you're using Django's built-in User model
    submission_date = models.DateTimeField(auto_now_add=True)
    text_submission = models.TextField(blank=True, null=True)

    # Add other fields for the assignment submission data
    # For example, you can add a file field for uploaded submissions:
    file_submission = models.FileField(upload_to="assignments/submissions/")

    def __str__(self):
        return f"Submission for Assignment: {self.assignment.title}, Course: {self.course.title}, User: {self.submitted_by.username}"


class  UserProfile(models.Model):
    uu_id = models.UUIDField(default=uuid.uuid4,  unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="./static/images/background-class.jpeg")
    bio = models.TextField(max_length=500, default="Ente your bio")
    courses = models.ManyToManyField(Course)

    paystack_key = models.CharField(max_length=250, default="pk_test_f9d4e9c4b70a553a45fd67aea9e4f1429de302cf")
    status  = models.CharField(
        max_length=20, choices=[("Instructor", "Instructor"), ("Student", "Student"),], blank=True, default="Student")
    
    def __str__(self):
        return self.user.username
  

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='profile_pics/')
#     bio = models.TextField(blank=True)
#     contact_info = models.CharField(max_length=100, blank=True)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=200, blank=True)
#     phone_number = models.CharField(max_length=20, blank=True)


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_text = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)


class Notification(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# class Message(models.Model):
#     sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class CourseEnrollment(models.Model):
    # User who is enrolling
    uu_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE
    )  
    enrollment_date = models.DateTimeField(
        auto_now_add=True
    )  
    is_enrolled = models.BooleanField(default=False)

    payment_reference = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title} on {self.enrollment_date}"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lessons_completed = models.PositiveIntegerField(default=0)

    def calculate_progress_percentage(self):
        if self.course.total_lessons > 0:
            return (self.lessons_completed / self.course.total_lessons) * 100
        else:
            return 0

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Progress"
