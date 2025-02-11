from django import forms
from .models import Quiz, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'duration']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
