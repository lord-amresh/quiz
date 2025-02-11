from django.urls import path
from .views import home, register, user_login, user_logout, create_quiz, take_quiz, leaderboard, quiz_list
from .views import quiz_result

urlpatterns = [
    path('', home, name='home'),  # ✅ Home page
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create_quiz/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('quizzes/', quiz_list, name='quiz_list'), # ✅ Quizzes Page
    path('quiz/<int:quiz_id>/result/', quiz_result, name='quiz_result'),
]
