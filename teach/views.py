from .context_processors import exercise_modification_context
from .models import Exercise, Answer, Category, Solved, Struggles
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, "teach/index.html")


def check_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    exercise_id = answer.exercise.id

    # if logged in save to db
    if request.user.is_authenticated:
        user = request.user
        solved = Solved.objects.filter(user=user, exercise=answer.exercise).first()
        if not solved:
            Solved.objects.create(
                user=user, exercise=answer.exercise, correct=answer.correct
            )
        else:
            solved.correct = answer.correct
            solved.save()

    if "solved_exercises" not in request.session:
        request.session["solved_exercises"] = {}

    request.session["solved_exercises"][str(exercise_id)] = answer.correct
    request.session.modified = True
    context = exercise_modification_context(request, exercise_id)
    return JsonResponse(
        {
            "correct": answer.correct,
            "exercise_id": exercise_id,
            **context,
        }
    )


def get_exercises_for_category(request, category_id):
    category = Category.objects.get(id=category_id)
    exercises = category.exercise_set.all().order_by("difficulty")
    context = {
        "category_name": category.name,
        "exercises": exercises,
        "category_grade": category.grade,
    }
    return render(request, "teach/category.html", context)


def reset_exercise_info(request, exercise_id):
    if request.method == "DELETE":
        if "solved_exercises" in request.session:
            request.session["solved_exercises"].pop(str(exercise_id), None)
            request.session.modified = True
            context = exercise_modification_context(request, exercise_id)
            return JsonResponse(
                {
                    "status": "reset",
                    **context,
                }
            )
    return JsonResponse({"error": "Method not supported"}, status=405)


def hard_exercises(request, exercise_id):
    if request.user.is_authenticated:
        if request.method == "DELETE":
            try:
                struggle = Struggles.objects.get(
                    student=request.user, exercise_id=exercise_id
                )
                struggle.delete()
                return JsonResponse({"status": "deleted"})
            except Struggles.DoesNotExist:
                return JsonResponse({"error": "Entry not found"}, status=404)

        elif request.method == "POST":
            _, _ = Struggles.objects.get_or_create(
                student=request.user, exercise_id=exercise_id
            )
            exercise = Exercise.objects.get(id=exercise_id)
            return JsonResponse({"status": "added", "text": str(exercise)})

        return JsonResponse({"error": "Method not supported"}, status=405)
    return JsonResponse({"error": "User is not logged in"}, status=401)


def go_to_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    category_id = exercise.category.id
    return redirect(reverse("teach-category", args=[category_id]))
