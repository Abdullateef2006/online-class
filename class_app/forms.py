from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField



class PaymentForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}),
    )


class AssignmentSubmissionForm(forms.Form):
    file_submission = forms.FileField(required=False)
    text_submission = forms.CharField(widget=forms.Textarea, required=False)


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already in use. Please use a different email."
            )
        return email
    
    


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["content"]


class EmailForm(forms.Form):
    subject = forms.CharField(label="Subject", max_length=100)
    message = forms.CharField(label="Message", widget=forms.Textarea)
    # Your_email = forms.EmailField(label="From Email")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "bio",
            'paystack_key'
        ]  # Add any additional fields you want to include in the form


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username"}
        ),
        help_text="<small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your Email Address"}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your First Name"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your Last Name"}
        )
    )
    captcha = CaptchaField()

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="<small><ul><li>Your password can't be too similar to your other personal information.</li>\
                                    <li>Your password must contain at least 8 characters.</li>\
                                    <li>Your password can't be a commonly used password.</li>\
                                    <li>Your password can't be entirely numeric.</li></ul></small>",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="<small>Enter the same password as before, for verification.</small>",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('user', 'uu_id', 'instructor', 'is_enrolled','students',)
        
        

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ('course',)
        
        
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('lesson', )