from rest_framework import serializers
from class_app.models import *


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
        
        
class CourseListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['uu_id','title', 'instructor', 'description', 'language', 'category', 'img', 'price', 'level']
        
        
        
class CourseDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['uu_id','title', 'instructor', 'description', 'language', 'category', 'img', 'price', 'level','learn',  ]
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserProfile
        fields  = "__all__"
    
    
class LessonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = '__all__'
        
        

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255, required=True)
    message = serializers.CharField(required=True)

    def validate_subject(self, value):
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty.")
        return value

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value
