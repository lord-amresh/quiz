from django.contrib import admin
from .models import Quiz, Question, QuizAttempt

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'get_correct_answer', 'explanation')  # Show correct answer & explanation
    list_filter = ('quiz',)
    search_fields = ('text',)

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)  # Register with custom admin settings
admin.site.register(QuizAttempt)
