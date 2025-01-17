from django.contrib import admin
from .models import UserProfile, Category, ChatMessage, Topic,  CourseEnrollment, Course, Lesson, Discussion, Comment, Assignment, Submission, Notification, AssignmentSubmission
admin.site.register(UserProfile)
# admin.site.register(Course)
# admin.site.register(Lesson)
admin.site.register(Discussion)
admin.site.register(Comment)
admin.site.register(Assignment)
admin.site.register(Submission)


admin.site.register(Notification)
# admin.site.register(Message)
# admin.site.register(AssignmentSubmission)
admin.site.register(CourseEnrollment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    '''Admin View for Topic'''

    list_display = ['lesson','title']
    list_filter = ['lesson','title']

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    '''Admin View for AssignmentSubmission'''

    list_display = ['submitted_by','assignment', 'course', 'file_submission']
    list_filter = ['assignment']
   

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp']  

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('title','id', 'instructor', 'price')
#     list_filter = ('instructor','price')
#     search_fields = ('title', 'instructor')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'user')  # Customize your display fields as needed

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user  # Set the current logged-in admin as the user
        super().save_model(request, obj, form, change)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('title','course')
    search_fields = ('title', 'course')




# Register your models here.
