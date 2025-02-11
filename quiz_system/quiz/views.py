from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizAttempt
from .forms import QuizForm, QuestionForm
from django.utils.timezone import now
from django.db.models import Max

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quiz_list')
    else:
        form = AuthenticationForm()
    return render(request, 'quiz/login.html', {'form': form})

def home(request):
    return render(request, 'quiz/home.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('login')
@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'form': form})

@login_required
def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form, 'quiz': quiz})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    if request.method == "POST":
        score = 0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option and int(selected_option) == question.correct_option:
                score += 1
        QuizAttempt.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect('quiz_result', quiz_id=quiz.id)

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def leaderboard(request):
    # ✅ Fetch only the highest score per user
    top_scores = QuizAttempt.objects.values('user__username').annotate(high_score=Max('score')).order_by('-high_score')

    return render(request, 'quiz/leaderboard.html', {'top_scores': top_scores})
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    # Get the latest attempt by the logged-in user
    latest_attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-timestamp').first()

    # Calculate percentage
    total_questions = questions.count()
    score = latest_attempt.score if latest_attempt else 0
    percentage = (score / total_questions * 100) if total_questions > 0 else 0

    # Determine CSS class for progress bar color
    if percentage >= 75:
        progress_class = "progress-green"  # Green
    elif percentage >= 50:
        progress_class = "progress-yellow"  # Yellow
    else:
        progress_class = "progress-red"  # Red

    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'questions': questions,
        'latest_attempt': latest_attempt,
        'percentage': percentage,
        'progress_class': progress_class  # Send CSS class name
    })