from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .utils import check_solution
from django.utils import timezone
from io import BytesIO
from .models import Course, Lecture, Exercise, Submission, Message

# Load environment variables

# Create your views here.

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            return HttpResponse("Passwords do not match")
        
        User.objects.create_user(username=uname, email=email, password=password)
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid credentials")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Initialize userid for both GET and POST requests
    userid = request.user.id

    if request.method == 'POST' and 'logout' in request.POST:
        return redirect('logout')

    # Pass the userid to the template context
    return render(request, 'dashboard.html', {'userid': userid})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# View for listing all lectures in a course
def lecture_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lectures = Lecture.objects.filter(course=course).prefetch_related('exercises')  # Ensure exercises are prefetched

    return render(request, 'lecture_list.html', {'lectures': lectures, 'course': course})

# View for displaying a specific lecture and its associated exercises
def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    exercises = Exercise.objects.filter(lecture=lecture)
    return render(request, 'lecture_detail.html', {'lecture': lecture, 'exercises': exercises})



@login_required
def submit_exercise(request, exercise_id):
    try:
        exercise = get_object_or_404(Exercise, id=exercise_id)
    except Http404:
        # Show toast notification when the exercise is not found
        messages.error(request, "Exercise not found!")
        return redirect('exercises')  # Redirect to a safe page, like the homepage

    feedback = None
    if request.method == "POST":
        user_solution = request.POST.get('solution')
        if user_solution:
            feedback = check_solution(user_solution)  # Your existing check_solution function
            Submission.objects.create(
                exercise=exercise,
                user=request.user,
                answer_text=user_solution,
                feedback=feedback,
                marks_obtained=feedback.count('great job') * 10  # Example logic for assigning marks
            )
            # Optionally set a success message
            messages.success(request, "Solution submitted successfully!")
    
    return render(request, 'submit_exercise.html', {'exercise': exercise, 'feedback': feedback})
@login_required
def marks_view(request):
    submissions = Submission.objects.filter(user=request.user)
    return render(request, 'marks.html', {'submissions': submissions})

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def collab_view(request):
    # Retrieve messages for the current user
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')

    # Get all users except the current user to populate the recipient dropdown
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        content = request.POST.get('content')

        try:
            recipient = User.objects.get(id=recipient_id)
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return redirect('collab')
        except User.DoesNotExist:
            return render(request, 'collab.html', {
                'error': 'User does not exist', 
                'received_messages': received_messages, 
                'sent_messages': sent_messages, 
                'users': users
            })

    return render(request, 'collab.html', {
        'received_messages': received_messages, 
        'sent_messages': sent_messages, 
        'users': users
    })
@login_required
def progress_tracking(request):
    # Example data processing - adjust according to your data
    total_exercises = Exercise.objects.count()
    completed_exercises = Submission.objects.filter(user=request.user).count()
    
    # Calculate progress percentage
    progress_percentage = (completed_exercises / total_exercises) * 100 if total_exercises > 0 else 0

    context = {
        'progress_percentage': int(progress_percentage),  # Convert to integer for display
        'current_year': timezone.now().year,
    }

    return render(request, 'progress_tracking.html', context)
# @login_required
# def lectures(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     lectures = Lecture.objects.filter(course=course)
#     return render(request, 'vedeo.html', {'lectures': lectures, 'course': course})

# @login_required
# def course_list(request):
#     courses = Course.objects.all()
#     return render(request, 'course_list.html', {'courses': courses})

# @login_required
# def lecture_detail(request, lecture_id):
#     lecture = get_object_or_404(Lecture, id=lecture_id)
#     exercises = Exercise.objects.filter(lecture=lecture)
#     return render(request, 'lecture_detail.html', {'lecture': lecture, 'exercises': exercises})

# @login_required
# def submit_exercise(request, exercise_id):
#     exercise = get_object_or_404(Exercise, id=exercise_id)
#     feedback = None
    
#     if request.method == "POST":
#         user_solution = request.POST.get('solution')
        
#         if user_solution:
#             feedback = check_solution(user_solution)  # Ensure this function is defined
#             Submission.objects.create(
#                 exercise=exercise,
#                 user=request.user,
#                 answer_text=user_solution,
#                 feedback=feedback,
#                 marks_obtained=feedback.count('great job') * 10  # Example logic
#             )
#             return redirect('marks')
    
#     return render(request, 'submit_exercise.html', {'exercise': exercise, 'feedback': feedback})

# @login_required
# def marks_page(request):
#     submissions = Submission.objects.filter(user=request.user)
#     return render(request, 'marks.html', {'submissions': submissions})

# @login_required
# def about(request):
#     return render(request, 'about.html')

# @login_required
# def quiz(request):
#     return render(request, 'quiz.html')


# def chatbot(request):
#     chatbot_response = None
#     api_key = 'sk-Fex_R2ELJyqU5gHSE86wxScY6Qu2OpXMSXDkTIK3qpT3BlbkFJIrbtZUB71aYUi6wJ4ZV9xYH01s6qRCzNaWoMls6QAA'
#     openai.api_key= api_key
#   # Ensure this is correctly set
    
#     if api_key and request.method == 'POST':
#         openai.api_key = api_key
#         user_input = request.POST.get('user_input')
        
#         try:
#             response = openai.completion.create(
#                 model="gpt-4",  # Ensure the model is correct
#                 messages=[{"role": "user", "content": user_input}],
#                 max_tokens=450,
#                 temperature=0.5
#             )
#             chatbot_response = response['choices'][0]['message']['content']
#         except Exception as e:
#             chatbot_response = f"An error occurred: {str(e)}"
    
#     return render(request, 'chatbot.html', {"response": chatbot_response})
