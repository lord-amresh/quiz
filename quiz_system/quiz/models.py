from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(choices=[(1, "Option 1"), (2, "Option 2"), (3, "Option 3"), (4, "Option 4")])

    explanation = models.TextField(blank=True, null=True)  # New field for explanation

    def __str__(self):
        return self.text
    
    def get_correct_answer(self):
        """ Returns the correct option text """
        return getattr(self, f"option{self.correct_option}")

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
