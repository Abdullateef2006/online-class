# Course Management Views
# def create_course(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         course = Course(title=title, description=description, instructor=request.user)
#         course.save()
#         messages.success(request, 'Course created successfully!')
#         return redirect('dashboard')
#     return render(request, 'create_course.html')





# Messaging Views
# def send_message(request, receiver_id):
#     receiver = get_object_or_404(User, id=receiver_id)

#     if request.method == 'POST':
#         message_text = request.POST.get('message')
#         if message_text:
#             message = Message(sender=request.user, receiver=receiver, message=message_text)
#             message.save()
#             messages.success(request, 'Message sent successfully!')
#             return redirect('user_messages', receiver_id=receiver.id)  # Redirect after sending the message

#     # Render the send_message.html template
#     return render(request, 'send_message.html', {'receiver': receiver})


# def user_messages(request, receiver_id):
#     receiver = get_object_or_404(User, id=receiver_id)
#     messages_sent = Message.objects.filter(sender=request.user, receiver=receiver)
#     messages_received = Message.objects.filter(sender=receiver, receiver=request.user)
#     messages_combined = (messages_sent | messages_received).order_by('created_at')
#     return render(request, 'user_messages.html', {'receiver': receiver, 'messages': messages_combined})




# Import your CourseEnrollment model

# def paystack_callback(request):
#     reference = request.GET.get('reference')

#     # Retrieve the corresponding CourseEnrollment based on the payment reference
#     try:
#         enrollment = CourseEnrollment.objects.get(payment_reference=reference)
#     except CourseEnrollment.DoesNotExist:
#         return HttpResponse('Invalid payment reference.')

#     # Verify the payment status with Paystack (Make a GET request to Paystack API)
#     verification_url = f'https://api.paystack.co/transaction/verify/{reference}'

#     # Define your Paystack secret key

#     headers = {
#         'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
#     }

#     response = requests.get(verification_url, headers=headers)
#     response_data = response.json()

#     if response_data['status']:
#         if response_data['data']['status'] == 'success':
#             # Mark the enrollment as paid
#             enrollment.is_paid = True
#             enrollment.save()

#             # Add the course to the user's enrolled courses
#             enrollment.user.enrolled_courses.add(enrollment.course)

#             # Redirect to the enrolled courses page (update 'enrolled_courses' with your URL name)
#             return redirect('enrolled_courses')
    
#     # If payment verification fails or the status is not 'success', handle accordingly
#     return HttpResponse('Payment failed. Please try again.')



# views.py


# def discussion_detail(request, course_id, discussion_id):
#     discussion = get_object_or_404(Discussion, id=discussion_id)
#     # Logic to display discussion details
#     return render(request, 'discussion_detail.html', {'discussion': discussion})


# Discussion Forums Views
# def create_discussion(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.method == 'POST':
#         title = request.POST['title']
#         discussion = Discussion(course=course, title=title)
#         discussion.save()
#         messages.success(request, 'Discussion created successfully!')
#         return redirect('course_detail', course_id=course.id)
#     return render(request, 'create_discussion.html', {'course': course})

# def create_comment(request, discussion_id):
#     discussion = get_object_or_404(Discussion, id=discussion_id)
#     if request.method == 'POST':
#         text = request.POST['text']
#         comment = Comment(discussion=discussion, author=request.user, text=text)
#         comment.save()
#         messages.success(request, 'Comment posted successfully!')
#     return redirect('discussion_detail', discussion_id=discussion.id)

# # Assignments and Assessments Views
# def create_assignment(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         due_date = request.POST['due_date']
#         max_score = request.POST['max_score']
#         assignment = Assignment(course=course, title=title, description=description, due_date=due_date, max_score=max_score)
#         assignment.save()
#         messages.success(request, 'Assignment created successfully!')
#         return redirect('course_detail', course_id=course.id)
#     return render(request, 'create_assignment.html', {'course': course})

# views.py