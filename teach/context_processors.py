from .models import Category, Exercise
from django.db.models import Case, When

# Define the order as a list
order = ['Liczby Naturalne', 'Liczby Całkowite, Liczby Wymierne',
         'Liczby Niewymierne', 'Ułamki Dziesiętne', 'Pierwiastek Kwadratowy',
         'Pierwiastek Sześcienny', 'Potęgi', 'Logarytmy', 'Procenty',
         'Zbiory', 'Przedziały', 'Wartość Bezwzględna',
         'Wyrażenia Algebraiczne', 'Wzory Skróconego Mnożenia',
         'Równania i Nierówności', 'Układy Równań', 'Funkcja', 'Funkcja Liniowa',
         'Funkcja Kwadratowa', 'Proporcjonalność Odwrotna', 'Kąty w Trójkącie',
         'Podobieństwo Trójkątów', 'Twierdzenie Talesa', 'Równanie Prostej',
         'Wzory Skróconego Mnożenia 2', 'Wielomiany', 'Wyrażenia Wymierne', 
         'Równania i Nierówności 2', 'Układy Równań 2', 'Funkcja Kwadratowa 2',
         'Optymalizacja', 'Funkcje Trygonometryczne', 'Trójkąty',
         'Kąty Środkowe i Kąty Wpisane', 'Okrąg Opisany i Okrąg Wpisany',
         'Twierdzenie Sinusów i Twierdzenie Cosinusów', 'Potęgi 2',
         'Logarytmy 2', 'Funkcja Wykładnicza', 'Funkcja Logarytmiczna', 
         'Ciągi', 'Ciąg Arytmetyczny', 'Ciąg Geometryczny', 
         'Odległości na Płaszczyźnie', 'Równanie Okręgu',
         'Wzajemne Położenie Prostej i Okręgu', 'Symetrie', 'Statystyka',
         'Reguły Mnożenia i Dodawania', 'Permutacje i Wariacje', 'Prawdopodobieństwo',
         'Wartość Oczekiwana', 'Graniastosłupy', 'Ostrosłupy', 'Kąty w Stereometrii',
         'Bryły Obrotowe']


def base_template_context(request):
    # Ordering by "order" list
    categories = Category.objects.filter(name__in=order).annotate(
    order=Case(
        *[When(name=cat_name, then=order.index(cat_name)) for cat_name in order],
        default=len(order)
    )).order_by('order')

    grades = ['One', 'Two', 'Three', 'Four']
    solved_exercises = request.session.get('solved_exercises', {})
    exercises = Exercise.objects.all()
    hard_exercises = []
    if request.user.is_authenticated:
        user = request.user
        user_struggles = user.struggles_set.all()
        for struggle in user_struggles:
            hard_exercises.append(struggle.exercise)
    
    progress = calculate_total_progress(exercises, solved_exercises)

    completed_exercises_ids = get_completed_exercises_ids(solved_exercises)
    completed_percent = {}
    completed_count_in_category = {}

    # Creating dictionary completed_percent to display stats in sidebar:
    # key - category name; type: str
    # value - percent; type: float, range: 0-100
    # i.e. {"Functions": 58.5}
    for category in categories:
        all_exercises_count = category.exercise_set.count()
        if all_exercises_count > 0:
            completed_exercises_in_category = category.exercise_set.filter(id__in=completed_exercises_ids).count()
            completed_count_in_category[category.name] = completed_exercises_in_category
            completed_percent[category.name] = int(completed_exercises_in_category / all_exercises_count * 100)
        else:
            completed_percent[category.name] = 0
            completed_count_in_category[category.name] = 0     
            
    return {
        'categories': categories,
        'grades': grades,
        'solved_exercises': solved_exercises,
        'exercises': exercises,
        'completed_percent': completed_percent,
        'progress': progress,
        'hard_exercises': hard_exercises,
        'completed_per_category': completed_count_in_category,
    }

    
def exercise_modification_context(request, exercise_id):
    exercises = Exercise.objects.all()
    exercise = Exercise.objects.get(id=exercise_id)
    category_id = exercise.category.id
    solved_exercises = request.session.get('solved_exercises')
    total_progress = calculate_total_progress(exercises, solved_exercises)
    completed_exercises_ids = get_completed_exercises_ids(solved_exercises)
    all_exercises_in_category = exercise.category.exercise_set.count()
    completed_exercises_in_category = exercise.category.exercise_set.filter(id__in=completed_exercises_ids).count()
    category_progress = int(completed_exercises_in_category/all_exercises_in_category * 100)
    return {
        'category_id': category_id,
        'total_progress': total_progress,
        'category_progress': category_progress,
    }
    
    
def calculate_total_progress(exercises, solved_exercises):
    max_points = 0
    points = 0
    for exercise in exercises:
        max_points += exercise.difficulty
        if solved_exercises.get(str(exercise.id)) == True:
            points += exercise.difficulty
    return int(points/max_points * 100) if max_points != 0 else 0


def get_completed_exercises_ids(solved_exercises):
    completed_exercises = []    
    for id in solved_exercises.keys():
        if solved_exercises.get(id) == True:
            completed_exercises.append(id)
    return completed_exercises
