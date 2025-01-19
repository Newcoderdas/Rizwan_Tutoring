from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Lecture(models.Model):
    course = models.ForeignKey(Course, related_name='lectures', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_url = models.URLField()

    def __str__(self):
        return self.title

class Exercise(models.Model):
    lecture = models.ForeignKey(Lecture, related_name='exercises', on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_solution = models.TextField(default='Default solution')

    def __str__(self):
        return self.question_text

class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    answer_image = models.ImageField(upload_to='submissions/', blank=True)
    feedback = models.TextField(blank=True)
    marks_obtained = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)  
    
    def __str__(self):
        return f"Submission by {self.user} for {self.exercise}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"
