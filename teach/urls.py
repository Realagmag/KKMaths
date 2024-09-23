from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='teach-home'),
    path('answer/<answer_id>', views.check_answer, name='answer'),
    path('category/<category_id>', views.get_exercises_for_category, name='teach-category'),
    path('reset/<exercise_id>', views.reset_exercise_info, name='reset_exercise'),
    path('hard/<exercise_id>', views.hard_exercises ,name='hard'),
    path('go-to-exercise/<exercise_id>', views.go_to_exercise),
]